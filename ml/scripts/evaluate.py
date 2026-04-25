"""
Evaluate a trained YOLOv11 model on the validation set.

Reports mAP@50, mAP@50:95, precision, recall and per-class metrics.
Optionally saves sample predictions to disk.

Usage:
    uv run python scripts/evaluate.py --weights runs/detect/train/weights/best.pt
    uv run python scripts/evaluate.py --weights best.pt --save-images
"""

from __future__ import annotations

import argparse
import json
import logging
from pathlib import Path

from ultralytics import YOLO

logging.basicConfig(level=logging.INFO, format="%(levelname)s | %(message)s")
_logger = logging.getLogger(__name__)

PROJECT_ROOT = Path(__file__).resolve().parent.parent


def main() -> None:
    parser = argparse.ArgumentParser(description="Evaluate YOLOv11 road sign model")
    parser.add_argument(
        "--weights",
        type=str,
        required=True,
        help="Path to trained model weights (.pt)",
    )
    parser.add_argument(
        "--data",
        type=str,
        default=str(PROJECT_ROOT / "data" / "dataset.yaml"),
        help="Path to dataset YAML",
    )
    parser.add_argument(
        "--imgsz",
        type=int,
        default=640,
        help="Inference image size",
    )
    parser.add_argument(
        "--conf",
        type=float,
        default=0.25,
        help="Confidence threshold",
    )
    parser.add_argument(
        "--iou",
        type=float,
        default=0.6,
        help="IoU threshold for NMS",
    )
    parser.add_argument(
        "--save-images",
        action="store_true",
        help="Save prediction visualisations",
    )
    parser.add_argument(
        "--output-dir",
        type=str,
        default=str(PROJECT_ROOT / "runs" / "evaluate"),
        help="Directory for evaluation outputs",
    )
    args = parser.parse_args()

    _logger.info(f"Loading model from {args.weights}…")
    model = YOLO(args.weights)

    _logger.info("Running validation…")
    metrics = model.val(
        data=args.data,
        imgsz=args.imgsz,
        conf=args.conf,
        iou=args.iou,
        save_json=True,
        project=args.output_dir,
        name="val",
        exist_ok=True,
    )

    summary = {
        "mAP50": float(metrics.box.map50),
        "mAP50-95": float(metrics.box.map),
        "precision": float(metrics.box.mp),
        "recall": float(metrics.box.mr),
        "per_class_ap50": {
            name: float(ap)
            for name, ap in zip(metrics.names.values(), metrics.box.ap50)
        },
    }

    _logger.info("\n" + "=" * 50)
    _logger.info("EVALUATION RESULTS")
    _logger.info("=" * 50)
    _logger.info(f"  mAP@50:      {summary['mAP50']:.4f}")
    _logger.info(f"  mAP@50:95:   {summary['mAP50-95']:.4f}")
    _logger.info(f"  Precision:   {summary['precision']:.4f}")
    _logger.info(f"  Recall:      {summary['recall']:.4f}")
    _logger.info("-" * 50)
    for cls_name, ap in summary["per_class_ap50"].items():
        _logger.info(f"  {cls_name:<15s}  AP@50: {ap:.4f}")
    _logger.info("=" * 50)

    output_path = Path(args.output_dir) / "val" / "metrics.json"
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "w") as f:
        json.dump(summary, f, indent=2)
    _logger.info(f"Metrics saved to {output_path}")

    if args.save_images:
        _logger.info("Generating sample predictions…")
        model.predict(
            source=str(PROJECT_ROOT / "datasets" / "gtsdb" / "images" / "val"),
            imgsz=args.imgsz,
            conf=args.conf,
            save=True,
            project=args.output_dir,
            name="predictions",
            exist_ok=True,
        )
        _logger.info(f"Predictions saved to {args.output_dir}/predictions/")


if __name__ == "__main__":
    main()

