import pytest
import numpy as np
import cv2

from backend.src.frame.domain.detection import DetectionResult

from .conftest import build_adapter, make_settings, make_onnx_output


class TestDetect:
    @pytest.mark.asyncio
    async def test_returns_none_for_invalid_image(self, adapter):
        result = await adapter.detect(b"garbage_bytes")

        assert result is None

    @pytest.mark.asyncio
    async def test_returns_detection_result(self, adapter):
        onnx_output = make_onnx_output(
            boxes=[[320, 320, 128, 64]],
            class_scores=[[0.0] * 14 + [0.92] + [0.0] * 28],
        )
        adapter._session.run.return_value = [onnx_output]

        image = np.zeros((100, 100, 3), dtype=np.uint8)
        _, encoded = cv2.imencode(".jpg", image)

        result = await adapter.detect(encoded.tobytes())

        assert result is not None
        assert isinstance(result, DetectionResult)
        assert result.sign_name == "stop"
        assert result.confidence == pytest.approx(0.92, abs=0.01)

    @pytest.mark.asyncio
    async def test_returns_none_when_no_detections(self):
        adapter = build_adapter(make_settings(confidence_threshold=0.99))
        onnx_output = make_onnx_output(
            boxes=[[320, 320, 100, 100]],
            class_scores=[[0.3] + [0.0] * 42],
        )
        adapter._session.run.return_value = [onnx_output]

        image = np.zeros((100, 100, 3), dtype=np.uint8)
        _, encoded = cv2.imencode(".jpg", image)

        result = await adapter.detect(encoded.tobytes())

        assert result is None

