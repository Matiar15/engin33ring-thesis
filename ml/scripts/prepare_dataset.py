"""
Download and prepare the GTSDB dataset for YOLO training.

Steps:
  1. Download GTSDB via kagglehub (or a direct URL fallback).
  2. Convert CSV annotations → YOLO .txt labels (43 fine-grained classes).
  3. Split into train / val sets (80/20).
  4. Arrange files in the YOLO directory layout expected by dataset.yaml.

Usage:
    uv run python scripts/prepare_dataset.py [--split-ratio 0.8]
"""

from __future__ import annotations

import argparse
import logging
import random
import shutil
from pathlib import Path

logging.basicConfig(level=logging.INFO, format="%(levelname)s | %(message)s")
_logger = logging.getLogger(__name__)

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATASET_DIR = PROJECT_ROOT / "datasets" / "gtsdb"


def download_gtsdb(dest: Path) -> Path:
    """Download GTSDB via kagglehub and return path to the extracted folder."""
    try:
        import kagglehub

        _logger.info("Downloading GTSDB from Kaggle…")
        path = kagglehub.dataset_download("safabouguezzi/german-traffic-sign-detection-benchmark-gtsdb")
        return Path(path)
    except Exception as e:
        _logger.error(
            f"kagglehub download failed: {e}\n"
            "Make sure you have configured Kaggle credentials.\n"
            "See: https://github.com/Kaggle/kagglehub#authenticate"
        )
        raise


def build_yolo_split(
    image_files: list[Path],
    annotations: dict[str, list[str]],
    images_dir: Path,
    labels_dir: Path,
) -> None:
    """Copy images and write YOLO label files for a single split."""
    images_dir.mkdir(parents=True, exist_ok=True)
    labels_dir.mkdir(parents=True, exist_ok=True)

    for img_path in image_files:
        shutil.copy2(img_path, images_dir / img_path.name)

        stem = img_path.stem
        label_file = labels_dir / f"{stem}.txt"
        lines = annotations.get(img_path.name, [])
        label_file.write_text("\n".join(lines) + "\n" if lines else "")


def main() -> None:
    parser = argparse.ArgumentParser(description="Prepare GTSDB for YOLO training")
    parser.add_argument(
        "--split-ratio",
        type=float,
        default=0.8,
        help="Train split ratio (default: 0.8)",
    )
    parser.add_argument(
        "--seed",
        type=int,
        default=42,
        help="Random seed for reproducible splits",
    )
    args = parser.parse_args()

    # ── 1. Download ──────────────────────────────────────────────
    raw_dir = download_gtsdb(DATASET_DIR / "raw")
    _logger.info(f"Dataset downloaded to: {raw_dir}")

    # Locate images and annotation CSV
    # kagglehub may nest files; search recursively
    image_files = sorted(raw_dir.rglob("*.ppm")) + sorted(raw_dir.rglob("*.png")) + sorted(raw_dir.rglob("*.jpg"))
    gt_csv_candidates = list(raw_dir.rglob("gt.txt"))

    if not image_files:
        raise FileNotFoundError(f"No images found in {raw_dir}")
    if not gt_csv_candidates:
        raise FileNotFoundError(f"No gt.txt annotation file found in {raw_dir}")

    gt_csv = gt_csv_candidates[0]
    _logger.info(f"Found {len(image_files)} images, annotations at {gt_csv}")

    # ── 2. Convert annotations ───────────────────────────────────
    from src.dataset_converter import convert_gtsdb_annotations

    # We'll collect annotations as dict, then distribute to splits
    _logger.info("Converting annotations to YOLO format…")
    annotations = convert_gtsdb_annotations(
        annotation_csv=gt_csv,
        output_labels_dir=DATASET_DIR / "_tmp_labels",
        image_width=1360,
        image_height=800,
    )

    # ── 3. Train / Val split ─────────────────────────────────────
    random.seed(args.seed)
    random.shuffle(image_files)
    split_idx = int(len(image_files) * args.split_ratio)
    train_images = image_files[:split_idx]
    val_images = image_files[split_idx:]

    _logger.info(f"Split: {len(train_images)} train / {len(val_images)} val")

    # ── 4. Build YOLO directory layout ───────────────────────────
    build_yolo_split(
        train_images,
        annotations,
        DATASET_DIR / "images" / "train",
        DATASET_DIR / "labels" / "train",
    )
    build_yolo_split(
        val_images,
        annotations,
        DATASET_DIR / "images" / "val",
        DATASET_DIR / "labels" / "val",
    )

    # Clean up temp labels
    shutil.rmtree(DATASET_DIR / "_tmp_labels", ignore_errors=True)

    _logger.info(
        f"✅ Dataset ready at {DATASET_DIR}\n"
        f"   images/train: {len(train_images)}\n"
        f"   images/val:   {len(val_images)}"
    )


if __name__ == "__main__":
    main()

