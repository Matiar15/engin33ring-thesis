import numpy as np
import pytest
from unittest.mock import MagicMock, patch

from backend.src.infrastructure.adapter.onnx_detection_adapter import (
    OnnxDetectionAdapter,
)
from backend.src.settings import DetectionSettings


def make_settings(**overrides) -> DetectionSettings:
    defaults = {
        "model_path": "fake.onnx",
        "input_size": 640,
        "confidence_threshold": 0.25,
        "iou_threshold": 0.45,
        "num_classes": 43,
    }
    defaults.update(overrides)
    return DetectionSettings(**defaults)


def build_adapter(settings: DetectionSettings | None = None) -> OnnxDetectionAdapter:
    settings = settings or make_settings()
    with patch("backend.src.infrastructure.adapter.onnx_detection_adapter.ort") as mock_ort:
        mock_session = MagicMock()
        mock_input = MagicMock()
        mock_input.name = "images"
        mock_session.get_inputs.return_value = [mock_input]
        mock_ort.InferenceSession.return_value = mock_session
        adapter = OnnxDetectionAdapter(settings=settings)
    return adapter


def make_onnx_output(
    boxes: list[list[float]],
    class_scores: list[list[float]],
) -> np.ndarray:
    """Build a fake ONNX output tensor [1, 4+C, N] from readable inputs."""
    boxes_arr = np.array(boxes, dtype=np.float32)
    scores_arr = np.array(class_scores, dtype=np.float32)
    combined = np.concatenate([boxes_arr, scores_arr], axis=1)
    return np.expand_dims(combined.T, axis=0)


@pytest.fixture
def adapter():
    return build_adapter()

