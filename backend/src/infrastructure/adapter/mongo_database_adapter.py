import logging
import pymongo

from pymongo.asynchronous.database import AsyncDatabase

from backend.src.infrastructure.port.database_port import DatabasePort
from backend.src.metadata.domain.metadata import Metadata
from backend.src.settings import Settings

_logger = logging.getLogger(__name__)


class MetadataMongoDatabaseAdapter(DatabasePort[Metadata]):
    def __init__(
        self,
        settings: Settings,
    ):
        connection_string = f"mongodb+srv://{settings.database.user}:{settings.database.password}@{settings.database.host}/{settings.database.name}"

        _logger.info(f"Connecting to MongoDB at {settings.database.host}...")
        self.mongo_client: AsyncDatabase[Metadata] = (
            pymongo.AsyncMongoClient(
                connection_string,
                maxPoolSize=20,
                maxIdleTimeMS=30_000,
            )
        )[settings.database.name]
        _logger.info("Connected to MongoDB.")
        self.collection_name = "metadata"

    async def create(self, domain: Metadata,) -> str:
        insert_one_result = await self.mongo_client[self.collection_name].insert_one(
            domain.model_dump(
                by_alias=True,
                exclude_unset=True,
            )
        )

        return str(insert_one_result.inserted_id)
