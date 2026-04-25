import numpy as np


class TestDecodeImage:
    def test_returns_none_for_invalid_bytes(self, adapter):
        result = adapter._decode_image(b"not_a_real_image")

        assert result is None

    def test_decodes_valid_jpeg(self, adapter):
        import cv2

        image = np.zeros((50, 50, 3), dtype=np.uint8)
        _, encoded = cv2.imencode(".jpg", image)

        result = adapter._decode_image(encoded.tobytes())

        assert result is not None
        assert result.shape[0] == 50
        assert result.shape[1] == 50
