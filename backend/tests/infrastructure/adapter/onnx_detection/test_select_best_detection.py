import pytest
import numpy as np

from backend.src.infrastructure.adapter.onnx_detection_adapter import (
    OnnxDetectionAdapter,
)

from .conftest import build_adapter, make_settings


class TestSelectBestDetection:
    def test_picks_first_nms_index(self):
        indices = np.array([2, 0, 1])
        scores = np.array([0.5, 0.7, 0.9])
        class_ids = np.array([0, 1, 14])
        boxes = np.array(
            [
                [100, 100, 50, 50],
                [200, 200, 60, 60],
                [300, 300, 70, 70],
            ],
            dtype=np.float32,
        )

        score, cls_id, box = OnnxDetectionAdapter._select_best_detection(
            indices,
            scores,
            class_ids,
            boxes,
        )

        assert score == pytest.approx(0.9)
        assert cls_id == 14
        np.testing.assert_array_equal(box, [300, 300, 70, 70])
