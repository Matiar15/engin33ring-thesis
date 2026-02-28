import logging

from backend.src.analysis.application.analysis_port import AnalysisPort
from backend.src.frame.application.frame_port import FramePort
from backend.src.frame.api.model import (
    FramePayload,
    FrameResponse,
    map_to_response,
)
from backend.src.frame.domain.frame import Frame

_logger = logging.getLogger(__name__)


class CreateFrameUseCase:
    def __init__(
        self,
        frame_port: FramePort,
        analysis_port: AnalysisPort,
    ):
        self.frame_port = frame_port
        self.analysis_port = analysis_port

    async def create(
        self,
        frame_payload: FramePayload,
    ) -> FrameResponse:
        _logger.info(f"Received frame payload: {frame_payload}")

        _logger.info(
            f"Validating existence of analysis with id: {frame_payload.analysis_id}..."
        )
        analysis = self.analysis_port.get_one(
            id=frame_payload.analysis_id, user_id=frame_payload.user_id
        )

        if not analysis:
            raise ValueError(
                f"Analysis with id: {frame_payload.analysis_id} does not exist."
            )

        _logger.info(
            f"Analysis with id: {frame_payload.analysis_id} exists. Proceeding with frame creation..."
        )

        _logger.info(f"Creating frame for user: {frame_payload.user_id}...")
        inserted_id: str = await self.frame_port.create(
            frame=Frame.from_payload(frame_payload.model_dump())
        )

        _logger.info(f"Frame created with id: {inserted_id}")
        return map_to_response()
