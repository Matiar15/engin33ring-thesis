import datetime
import logging

from backend.src.analysis.application.analysis_port import AnalysisPort
from backend.src.frame.api.model import (
    FramePayload,
    FrameResponse,
    map_to_response,
)
from backend.src.frame.application.detection_port import DetectionPort
from backend.src.frame.domain.frame import Frame
from backend.src.long_term_storage.application.long_term_storage_port import (
    LongTermStoragePort,
)

_logger = logging.getLogger(__name__)


class CreateFrameUseCase:
    def __init__(
        self,
        analysis_port: AnalysisPort,
        long_term_storage_port: LongTermStoragePort,
        detection_port: DetectionPort,
    ):
        self.analysis_port = analysis_port
        self.long_term_storage_port = long_term_storage_port
        self.detection_port = detection_port

    async def create(
        self,
        frame_payload: FramePayload,
    ) -> FrameResponse:
        _logger.info(f"Received frame payload: {frame_payload}")

        _logger.info(
            f"Validating existence of analysis with id: {frame_payload.analysis_id}..."
        )
        analysis = await self.analysis_port.get_one(
            id=frame_payload.analysis_id,
            user_id=frame_payload.user_id,
            statuses=[
                "created",
                "processing",
            ],
        )

        if not analysis:
            raise ValueError(
                f"Analysis with id: {frame_payload.analysis_id} does not exist."
            )

        _logger.info(
            f"Analysis with id: {frame_payload.analysis_id} exists. Proceeding with frame creation..."
        )

        # Read image bytes before storing (store_file consumes the stream)
        image_bytes = await frame_payload.frame.read()
        await frame_payload.frame.seek(0)

        _logger.info(f"Storing frame file...")
        frame_url = await self.long_term_storage_port.store_file(
            frame_payload.frame.file,
            bucket_name="engin33ring-thesis-frames",
            naming_strategy=f"{frame_payload.user_id}/{frame_payload.analysis_id}/{frame_payload.incoming_id}_",
            format="jpg",
        )
        _logger.info(f"Frame file stored at: {frame_url}")

        _logger.info(f"Running detection on frame...")
        detection = await self.detection_port.detect(image_bytes)

        if detection is None:
            _logger.info("No sign detected in frame.")
            response = FrameResponse(
                sign="NO_DETECTION",
                bounding_box={"x": 0, "y": 0, "width": 0, "height": 0},
                confidence=0,
            )
        else:
            _logger.info(f"Detected sign: {detection.sign_name} ({detection.confidence:.2f})")
            response = map_to_response(detection)

        await self.analysis_port.update(
            id=str(analysis.id),
            frame=Frame.from_payload(
                {
                    "id": frame_payload.incoming_id,
                    "frame_url": frame_url,
                    "created_at": datetime.datetime.now(),
                    "sign": response.sign,
                    "x": response.bounding_box.x,
                    "y": response.bounding_box.y,
                    "width": response.bounding_box.width,
                    "height": response.bounding_box.height,
                }
            ),
            status="processing",
        )

        return response
