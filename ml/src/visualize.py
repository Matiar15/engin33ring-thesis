"""
Visualisation helpers – draw bounding boxes and labels on images.
"""

from __future__ import annotations

from pathlib import Path

import cv2
import numpy as np

from src.label_mapping import (
    GTSDB_FINE_NAMES,
    GTSDB_CLASS_TO_SUPERCATEGORY,
)

# Distinct colours per super-category (BGR)
_SUPERCATEGORY_COLOURS: dict[int, tuple[int, int, int]] = {
    0: (0, 0, 255),      # prohibitory → red
    1: (255, 128, 0),    # mandatory   → blue
    2: (0, 200, 255),    # danger      → yellow
    3: (200, 200, 200),  # other       → grey
}


def _colour_for_class(cls_id: int) -> tuple[int, int, int]:
    """Get box colour based on the super-category of a fine-grained class."""
    super_id = GTSDB_CLASS_TO_SUPERCATEGORY.get(cls_id, -1)
    return _SUPERCATEGORY_COLOURS.get(super_id, (255, 255, 255))


def draw_yolo_boxes(
    image: np.ndarray,
    label_path: Path,
    line_thickness: int = 2,
) -> np.ndarray:
    """
    Draw YOLO-format bounding boxes on an image.

    Parameters
    ----------
    image : np.ndarray
        BGR image loaded via cv2.
    label_path : Path
        Path to a YOLO .txt label file.
    line_thickness : int
        Box line thickness in pixels.

    Returns
    -------
    np.ndarray
        Image with drawn boxes.
    """
    h, w = image.shape[:2]
    output = image.copy()

    if not label_path.exists():
        return output

    for line in label_path.read_text().strip().splitlines():
        parts = line.strip().split()
        if len(parts) < 5:
            continue

        cls_id = int(parts[0])
        xc, yc, bw, bh = (float(p) for p in parts[1:5])

        # Denormalise
        x1 = int((xc - bw / 2) * w)
        y1 = int((yc - bh / 2) * h)
        x2 = int((xc + bw / 2) * w)
        y2 = int((yc + bh / 2) * h)

        colour = _colour_for_class(cls_id)
        label = GTSDB_FINE_NAMES.get(cls_id, str(cls_id))

        cv2.rectangle(output, (x1, y1), (x2, y2), colour, line_thickness)

        # Label background
        (tw, th), _ = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.6, 1)
        cv2.rectangle(output, (x1, y1 - th - 6), (x1 + tw + 4, y1), colour, -1)
        cv2.putText(
            output,
            label,
            (x1 + 2, y1 - 4),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.6,
            (255, 255, 255),
            1,
            cv2.LINE_AA,
        )

    return output


def visualise_predictions(
    image: np.ndarray,
    results: list,
    confidence_threshold: float = 0.25,
    line_thickness: int = 2,
) -> np.ndarray:
    """
    Draw Ultralytics prediction results on an image.

    Parameters
    ----------
    image : np.ndarray
        BGR image.
    results : list
        Ultralytics Results objects (from model.predict()).
    confidence_threshold : float
        Minimum confidence to draw a box.
    line_thickness : int
        Box line thickness.

    Returns
    -------
    np.ndarray
        Annotated image.
    """
    output = image.copy()

    for result in results:
        boxes = result.boxes
        if boxes is None:
            continue

        for box in boxes:
            conf = float(box.conf[0])
            if conf < confidence_threshold:
                continue

            cls_id = int(box.cls[0])
            x1, y1, x2, y2 = (int(v) for v in box.xyxy[0])

            colour = _colour_for_class(cls_id)
            label_text = f"{GTSDB_FINE_NAMES.get(cls_id, str(cls_id))} {conf:.2f}"

            cv2.rectangle(output, (x1, y1), (x2, y2), colour, line_thickness)

            (tw, th), _ = cv2.getTextSize(
                label_text, cv2.FONT_HERSHEY_SIMPLEX, 0.6, 1
            )
            cv2.rectangle(
                output, (x1, y1 - th - 6), (x1 + tw + 4, y1), colour, -1
            )
            cv2.putText(
                output,
                label_text,
                (x1 + 2, y1 - 4),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.6,
                (255, 255, 255),
                1,
                cv2.LINE_AA,
            )

    return output

