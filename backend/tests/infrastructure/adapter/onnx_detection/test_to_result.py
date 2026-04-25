import pytest
import numpy as np

from backend.src.frame.domain.detection import DetectionResult

from .conftest import build_adapter, make_settings


class TestToResult:
    def test_converts_box_to_percentages(self):
        adapter = build_adapter(make_settings(input_size=640))
        box = np.array([320.0, 320.0, 128.0, 64.0])

        result = adapter._to_result(0.85, 1, box)

        assert isinstance(result, DetectionResult)
        assert result.sign_name == "speed_limit_30"
        assert result.confidence == pytest.approx(0.85)
        assert result.x == pytest.approx((320 - 64) / 640 * 100)
        assert result.y == pytest.approx((320 - 32) / 640 * 100)
        assert result.width == pytest.approx(128 / 640 * 100)
        assert result.height == pytest.approx(64 / 640 * 100)

    def test_unknown_class_id(self, adapter):
        box = np.array([100.0, 100.0, 50.0, 50.0])

        result = adapter._to_result(0.5, 999, box)

        assert result.sign_name == "unknown_999"
