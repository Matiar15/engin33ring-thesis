import logging

from backend.src.infrastructure.port.database_port import DatabasePort
from backend.src.metadata.api.model import (
    MetadataRequest,
    MetadataResponse,
    map_to_response,
)
from backend.src.metadata.domain.metadata import Metadata

_logger = logging.getLogger(__name__)


class MetadataUseCase:
    def __init__(
        self,
        database_port: DatabasePort[Metadata],
    ):
        self.database_port = database_port
        self.collection_name = "metadata"

    async def create(self, metadata_request: MetadataRequest) -> MetadataResponse:
        metadata = Metadata()

        _logger.info(f"Creating metadata with name: {metadata_request.name}...")
        result: Metadata = await self.database_port.create(
            collection_name=self.collection_name,
            domain=metadata,
        )

        _logger.info(f"Metadata created with id: {result.id}")
        return map_to_response(result)
