"""
Export a trained YOLOv11 model to ONNX (and optionally TorchScript).

The exported model can be served via ONNX Runtime in the backend for inference
without requiring the full PyTorch / Ultralytics stack.

Usage:
    uv run python scripts/export_model.py --weights runs/detect/train/weights/best.pt
    uv run python scripts/export_model.py --weights best.pt --format onnx --imgsz 640
"""

from __future__ import annotations

import argparse
import logging
from pathlib import Path

from ultralytics import YOLO

logging.basicConfig(level=logging.INFO, format="%(levelname)s | %(message)s")
_logger = logging.getLogger(__name__)


def main() -> None:
    parser = argparse.ArgumentParser(description="Export YOLOv11 to ONNX")
    parser.add_argument(
        "--weights",
        type=str,
        required=True,
        help="Path to trained model weights (.pt)",
    )
    parser.add_argument(
        "--format",
        type=str,
        default="onnx",
        choices=["onnx", "torchscript", "openvino", "engine"],
        help="Export format (default: onnx)",
    )
    parser.add_argument(
        "--imgsz",
        type=int,
        default=640,
        help="Input image size for the exported model",
    )
    parser.add_argument(
        "--half",
        action="store_true",
        help="Export with FP16 half precision",
    )
    parser.add_argument(
        "--dynamic",
        action="store_true",
        help="Enable dynamic axes for ONNX (variable batch size)",
    )
    parser.add_argument(
        "--simplify",
        action="store_true",
        default=True,
        help="Simplify ONNX graph (default: True)",
    )
    args = parser.parse_args()

    weights_path = Path(args.weights)
    if not weights_path.exists():
        raise FileNotFoundError(f"Model weights not found: {weights_path}")

    _logger.info(f"Loading model from {weights_path}…")
    model = YOLO(str(weights_path))

    _logger.info(f"Exporting to {args.format.upper()}…")
    export_path = model.export(
        format=args.format,
        imgsz=args.imgsz,
        half=args.half,
        dynamic=args.dynamic,
        simplify=args.simplify,
    )

    _logger.info(f"✅ Model exported to: {export_path}")

    # Validate exported model
    if args.format == "onnx":
        try:
            import onnx

            onnx_model = onnx.load(export_path)
            onnx.checker.check_model(onnx_model)
            _logger.info("ONNX model validation: ✅ passed")
        except Exception as e:
            _logger.warning(f"ONNX validation warning: {e}")


if __name__ == "__main__":
    main()

