import logging

from backend.src.analysis.application.analysis_port import AnalysisPort
from backend.src.analysis.domain.analysis import Analysis

_logger = logging.getLogger(__name__)


class GetAnalysisListUseCase:
    def __init__(self, analysis_port: AnalysisPort):
        self.analysis_port = analysis_port

    async def get_list(
        self,
        user_id: str,
        limit: int = 10,
        offset: int = 0,
    ) -> list[Analysis]:
        _logger.info(f"Getting analysis list for user: {user_id}...")
        return await self.analysis_port.get_list(
            user_id=user_id,
            limit=limit,
            offset=offset,
        )
