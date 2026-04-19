"""
Train YOLOv11 on the GTSDB dataset for road sign detection.

Reads hyperparameters from configs/train_config.yaml and kicks off
Ultralytics fine-tuning.

Usage:
    uv run python scripts/train.py
    uv run python scripts/train.py --config configs/train_config.yaml
    uv run python scripts/train.py --epochs 50 --batch 32   # CLI overrides
"""

from __future__ import annotations

import argparse
import logging
from pathlib import Path

import yaml
from ultralytics import YOLO

logging.basicConfig(level=logging.INFO, format="%(levelname)s | %(message)s")
_logger = logging.getLogger(__name__)

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_CONFIG = PROJECT_ROOT / "configs" / "train_config.yaml"


def load_config(config_path: Path) -> dict:
    """Load YAML training config."""
    with open(config_path, "r") as f:
        cfg = yaml.safe_load(f)
    _logger.info(f"Loaded config from {config_path}")
    return cfg


def main() -> None:
    parser = argparse.ArgumentParser(description="Train YOLOv11 on GTSDB")
    parser.add_argument(
        "--config",
        type=Path,
        default=DEFAULT_CONFIG,
        help="Path to training config YAML",
    )
    # Allow CLI overrides for common params
    parser.add_argument("--model", type=str, default=None)
    parser.add_argument("--epochs", type=int, default=None)
    parser.add_argument("--batch", type=int, default=None)
    parser.add_argument("--imgsz", type=int, default=None)
    parser.add_argument("--device", type=str, default=None)
    args = parser.parse_args()

    # ── Load config ──────────────────────────────────────────────
    cfg = load_config(args.config)

    # CLI overrides
    if args.model is not None:
        cfg["model"] = args.model
    if args.epochs is not None:
        cfg["epochs"] = args.epochs
    if args.batch is not None:
        cfg["batch"] = args.batch
    if args.imgsz is not None:
        cfg["imgsz"] = args.imgsz
    if args.device is not None:
        cfg["device"] = args.device

    # Resolve dataset.yaml path relative to project root
    data_path = cfg.pop("data", "data/dataset.yaml")
    data_abs = (PROJECT_ROOT / data_path).resolve()
    if not data_abs.exists():
        raise FileNotFoundError(
            f"Dataset config not found: {data_abs}\n"
            "Run `python scripts/prepare_dataset.py` first."
        )

    model_name = cfg.pop("model", "yolo11n.pt")

    _logger.info(f"Base model: {model_name}")
    _logger.info(f"Dataset config: {data_abs}")
    _logger.info(f"Training params: {cfg}")

    # ── Load pre-trained model ───────────────────────────────────
    model = YOLO(model_name)

    # ── Train ────────────────────────────────────────────────────
    results = model.train(
        data=str(data_abs),
        **cfg,
    )

    _logger.info("✅ Training complete!")
    _logger.info(f"Best weights: {Path(cfg.get('project', 'runs/detect')) / cfg.get('name', 'train') / 'weights' / 'best.pt'}")

    return results


if __name__ == "__main__":
    main()
