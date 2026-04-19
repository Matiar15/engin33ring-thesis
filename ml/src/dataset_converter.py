"""
Converter: GTSDB CSV annotations → YOLO TXT format.

GTSDB annotation format (CSV, semicolon-separated):
    filename;x1;y1;x2;y2;class_id

YOLO format (one .txt per image):
    class_id x_center y_center width height
    (all values normalised to [0, 1])

Uses all 43 fine-grained GTSDB class IDs directly as YOLO labels.
"""

from __future__ import annotations

import csv
import logging
from pathlib import Path

from src.label_mapping import VALID_GTSDB_IDS

_logger = logging.getLogger(__name__)


def convert_gtsdb_annotations(
    annotation_csv: Path,
    output_labels_dir: Path,
    image_width: int = 1360,
    image_height: int = 800,
) -> dict[str, list[str]]:
    """
    Read GTSDB ground-truth CSV and write per-image YOLO label files.

    Uses the original GTSDB class ID (0–42) directly as the YOLO class ID
    so the model learns to distinguish all 43 traffic sign types.

    Returns a dict mapping image filename → list of YOLO annotation lines.
    """
    output_labels_dir.mkdir(parents=True, exist_ok=True)

    annotations: dict[str, list[str]] = {}

    with open(annotation_csv, "r") as f:
        first_line = f.readline().strip()
        f.seek(0)

        # Auto-detect delimiter
        delimiter = ";" if ";" in first_line else ","

        # Skip header if present
        has_header = not first_line[0].isdigit() and not first_line.startswith("0")

        reader = csv.reader(f, delimiter=delimiter)
        if has_header:
            next(reader, None)

        for row in reader:
            if len(row) < 6:
                continue

            filename = row[0].strip()
            try:
                x1, y1, x2, y2 = int(row[1]), int(row[2]), int(row[3]), int(row[4])
                fine_class_id = int(row[5])
            except ValueError:
                _logger.warning(f"Skipping malformed row: {row}")
                continue

            if fine_class_id not in VALID_GTSDB_IDS:
                _logger.warning(
                    f"Skipping unknown class {fine_class_id} in {filename}"
                )
                continue

            # Use the fine-grained class ID directly (identity mapping)
            yolo_class_id = fine_class_id

            # Ensure correct coordinate ordering
            if x1 > x2:
                x1, x2 = x2, x1
            if y1 > y2:
                y1, y2 = y2, y1

            # Convert to YOLO normalised format
            x_center = ((x1 + x2) / 2.0) / image_width
            y_center = ((y1 + y2) / 2.0) / image_height
            box_width = (x2 - x1) / image_width
            box_height = (y2 - y1) / image_height

            # Clamp to [0, 1]
            x_center = max(0.0, min(1.0, x_center))
            y_center = max(0.0, min(1.0, y_center))
            box_width = max(0.0, min(1.0, box_width))
            box_height = max(0.0, min(1.0, box_height))

            # Skip degenerate boxes
            if box_width < 1e-6 or box_height < 1e-6:
                _logger.warning(
                    f"Skipping degenerate box in {filename}: "
                    f"w={box_width:.6f}, h={box_height:.6f}"
                )
                continue

            line = f"{yolo_class_id} {x_center:.6f} {y_center:.6f} {box_width:.6f} {box_height:.6f}"

            annotations.setdefault(filename, []).append(line)

    # Write label files
    for image_filename, lines in annotations.items():
        stem = Path(image_filename).stem
        label_path = output_labels_dir / f"{stem}.txt"
        label_path.write_text("\n".join(lines) + "\n")

    _logger.info(
        f"Converted {sum(len(v) for v in annotations.values())} annotations "
        f"across {len(annotations)} images → {output_labels_dir}"
    )
    return annotations

