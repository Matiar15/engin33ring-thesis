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
        inserted_id: str = await self.database_port.create(domain=metadata)

        _logger.info(f"Metadata created with id: {inserted_id}")
        return map_to_response(inserted_id)
