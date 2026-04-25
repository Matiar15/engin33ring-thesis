import abc

from backend.src.frame.domain.detection import DetectionResult


class DetectionPort(abc.ABC):
    @abc.abstractmethod
    async def detect(
        self,
        image_bytes: bytes,
    ) -> DetectionResult | None:
        """Run object detection on raw image bytes.

        Returns DetectionResult with the highest-confidence detection,
        or None if no sign was detected.
        """
