import logging

from backend.src.analysis.application.analysis_port import AnalysisPort
from backend.src.long_term_storage.application.long_term_storage_port import (
    LongTermStoragePort,
)

_logger = logging.getLogger(__name__)


class GetVideoUrlUseCase:
    def __init__(
        self,
        analysis_port: AnalysisPort,
        long_term_storage_port: LongTermStoragePort,
        bucket_name: str,
    ):
        self.analysis_port = analysis_port
        self.long_term_storage_port = long_term_storage_port
        self.bucket_name = bucket_name

    async def get_url(self, id: str, user_id: str) -> str | None:
        _logger.info(f"Getting video url for analysis {id} and user {user_id}")
        analysis = await self.analysis_port.get_one(id=id, user_id=user_id)
        if not analysis or not analysis.video_url:
            return None

        return await self.long_term_storage_port.generate_presigned_url(
            bucket_name=self.bucket_name,
            object_name=analysis.video_url,
            expiration=900,
        )
