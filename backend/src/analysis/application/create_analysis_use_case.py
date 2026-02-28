import logging

from backend.src.analysis.api.model import AnalysisPayload
from backend.src.analysis.application.analysis_port import AnalysisPort
from backend.src.analysis.domain.analysis import Analysis
from backend.src.frame.api.model import (
    FrameResponse,
    map_to_response,
)

_logger = logging.getLogger(__name__)


class CreateAnalysisUseCase:
    def __init__(
        self,
        analysis_port: AnalysisPort,
    ):
        self.analysis_port = analysis_port

    async def create(self, analysis_payload: AnalysisPayload) -> FrameResponse:
        _logger.info(f"Creating analysis for user: {analysis_payload.user_id}...")
        inserted_id: str = await self.analysis_port.create(
            analysis=Analysis.from_payload(analysis_payload.model_dump())
        )

        _logger.info(f"Frame created with id: {inserted_id}")
        return map_to_response()
