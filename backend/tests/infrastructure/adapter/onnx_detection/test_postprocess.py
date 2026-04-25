import pytest
import numpy as np

from .conftest import build_adapter, make_settings, make_onnx_output


class TestPostprocess:
    def test_returns_none_when_all_scores_below_threshold(self):
        adapter = build_adapter(make_settings(confidence_threshold=0.5))
        output = make_onnx_output(
            boxes=[[320, 320, 100, 100]],
            class_scores=[[0.1] * 43],
        )
        predictions = np.squeeze(output, axis=0).T

        result = adapter._postprocess(predictions)

        assert result is None

    def test_returns_best_detection(self):
        adapter = build_adapter(make_settings(confidence_threshold=0.25))
        output = make_onnx_output(
            boxes=[[320, 320, 100, 100], [100, 100, 50, 50]],
            class_scores=[
                [0.0] * 1 + [0.9] + [0.0] * 41,
                [0.5] + [0.0] * 42,
            ],
        )
        predictions = np.squeeze(output, axis=0).T

        result = adapter._postprocess(predictions)

        assert result is not None
        score, class_id, box = result
        assert score == pytest.approx(0.9)
        assert class_id == 1

    def test_filters_low_confidence_keeps_high(self):
        adapter = build_adapter(make_settings(confidence_threshold=0.6))
        output = make_onnx_output(
            boxes=[[320, 320, 100, 100], [100, 100, 50, 50]],
            class_scores=[
                [0.8] + [0.0] * 42,
                [0.3] + [0.0] * 42,
            ],
        )
        predictions = np.squeeze(output, axis=0).T

        result = adapter._postprocess(predictions)

        assert result is not None
        score, class_id, _ = result
        assert score == pytest.approx(0.8)
        assert class_id == 0
