import pytest
import numpy as np

from .conftest import build_adapter, make_settings


class TestPreprocess:
    def test_output_shape(self, adapter):
        image = np.zeros((480, 640, 3), dtype=np.uint8)

        blob = adapter._preprocess(image)

        assert blob.shape == (1, 3, 640, 640)
        assert blob.dtype == np.float32

    def test_pixel_values_normalized(self, adapter):
        image = np.full((100, 100, 3), 255, dtype=np.uint8)

        blob = adapter._preprocess(image)

        assert blob.max() == pytest.approx(1.0)

    def test_custom_input_size(self):
        adapter = build_adapter(make_settings(input_size=320))
        image = np.zeros((480, 640, 3), dtype=np.uint8)

        blob = adapter._preprocess(image)

        assert blob.shape == (1, 3, 320, 320)
