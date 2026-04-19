from __future__ import annotations

import asyncio
import logging

import cv2
import numpy as np
import onnxruntime as ort

from backend.src.frame.application.detection_port import DetectionPort
from backend.src.frame.domain.detection import DetectionResult
from backend.src.frame.domain.label_mapping import GTSDB_FINE_NAMES
from backend.src.settings import DetectionSettings

_logger = logging.getLogger(__name__)


class OnnxDetectionAdapter(DetectionPort):
    """ONNX Runtime adapter for YOLOv11 traffic sign detection."""

    def __init__(self, settings: DetectionSettings,) -> None:
        _logger.info(f"Loading ONNX model from {settings.model_path}...")
        self._session = ort.InferenceSession(
            settings.model_path,
            providers=["CPUExecutionProvider"],
        )
        self._input_name = self._session.get_inputs()[0].name
        self._input_size = settings.input_size
        self._confidence_threshold = settings.confidence_threshold
        self._iou_threshold = settings.iou_threshold
        self._num_classes = settings.num_classes
        _logger.info(
            f"ONNX model loaded (input_size={self._input_size}, "
            f"conf={self._confidence_threshold}, iou={self._iou_threshold}, "
            f"classes={self._num_classes})."
        )

    async def detect(self, image_bytes: bytes,) -> DetectionResult | None:
        return await asyncio.to_thread(self._detect_sync, image_bytes)

    def _detect_sync(self, image_bytes: bytes) -> DetectionResult | None:
        image = self._decode_image(image_bytes)
        if image is None:
            return None

        blob = self._preprocess(image)
        predictions = self._run_inference(blob)
        best = self._postprocess(predictions)

        if best is None:
            return None

        return self._to_result(*best)

    def _decode_image(self, image_bytes: bytes,) -> np.ndarray | None:  # noqa
        image_array = np.frombuffer(image_bytes, dtype=np.uint8)
        image = cv2.imdecode(image_array, cv2.IMREAD_COLOR)
        if image is None:
            _logger.warning("Failed to decode image bytes.")
        return image

    def _preprocess(self, image: np.ndarray) -> np.ndarray:
        resized = cv2.resize(image, (self._input_size, self._input_size))
        rgb = cv2.cvtColor(resized, cv2.COLOR_BGR2RGB)
        blob = rgb.astype(np.float32) / 255.0
        blob = np.transpose(blob, (2, 0, 1))
        return np.expand_dims(blob, axis=0)

    def _run_inference(self, blob: np.ndarray) -> np.ndarray:
        outputs = self._session.run(None, {self._input_name: blob})
        predictions = np.squeeze(outputs[0], axis=0)
        return predictions.T

    def _postprocess(
        self, predictions: np.ndarray,
    ) -> tuple[float, int, np.ndarray] | None:
        boxes_xywh = predictions[:, :4]
        class_scores = predictions[:, 4:]

        max_scores = np.max(class_scores, axis=1)
        class_ids = np.argmax(class_scores, axis=1)

        mask = max_scores >= self._confidence_threshold
        if not np.any(mask):
            _logger.info("No detections above confidence threshold.")
            return None

        filtered_boxes = boxes_xywh[mask]
        filtered_scores = max_scores[mask]
        filtered_class_ids = class_ids[mask]

        nms_indices = self._apply_nms(filtered_boxes, filtered_scores)
        if len(nms_indices) == 0:
            _logger.info("No detections after NMS.")
            return None

        return self._select_best_detection(
            nms_indices, filtered_scores, filtered_class_ids, filtered_boxes
        )

    def _apply_nms(
        self, boxes: np.ndarray, scores: np.ndarray,
    ) -> np.ndarray:
        x1 = boxes[:, 0] - boxes[:, 2] / 2
        y1 = boxes[:, 1] - boxes[:, 3] / 2
        nms_boxes = np.stack([x1, y1, boxes[:, 2], boxes[:, 3]], axis=1).tolist()

        return cv2.dnn.NMSBoxes(
            nms_boxes,
            scores.tolist(),
            self._confidence_threshold,
            self._iou_threshold,
        )

    @staticmethod
    def _select_best_detection(
        indices: np.ndarray,
        scores: np.ndarray,
        class_ids: np.ndarray,
        boxes: np.ndarray,
    ) -> tuple[float, int, np.ndarray]:
        best_idx = int(indices[0])
        return float(scores[best_idx]), int(class_ids[best_idx]), boxes[best_idx]

    def _to_result(
        self, score: float, class_id: int, box_xywh: np.ndarray,
    ) -> DetectionResult:
        xc, yc, bw, bh = box_xywh
        sz = self._input_size

        x_pct = float((xc - bw / 2) / sz * 100)
        y_pct = float((yc - bh / 2) / sz * 100)
        w_pct = float(bw / sz * 100)
        h_pct = float(bh / sz * 100)

        sign_name = GTSDB_FINE_NAMES.get(class_id, f"unknown_{class_id}")

        _logger.info(
            f"Detected: {sign_name} (class={class_id}, "
            f"conf={score:.2f}, box=[{x_pct:.1f}%, {y_pct:.1f}%, {w_pct:.1f}%, {h_pct:.1f}%])"
        )

        return DetectionResult(
            sign_name=sign_name,
            confidence=score,
            x=x_pct,
            y=y_pct,
            width=w_pct,
            height=h_pct,
        )
