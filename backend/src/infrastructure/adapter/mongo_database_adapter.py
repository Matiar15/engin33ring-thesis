import typing

import pymongo

from backend.src.infrastructure.port.database_port import DatabasePort
from backend.src.metadata.domain.metadata import Metadata
from backend.src.settings import Settings

T = typing.TypeVar("T")


class MetadataMongoDatabaseAdapter(DatabasePort[Metadata]):
    def __init__(
        self,
        settings: Settings,
    ):
        connection_string = f"mongodb+srv://{settings.database.user}:{settings.database.password}@{settings.database.host}/{settings.database.name}"
        self.mongo_client: pymongo.AsyncMongoClient[Metadata] = (
            pymongo.AsyncMongoClient(
                connection_string,
                maxPoolSize=20,
                maxIdleTimeMS=30_000,
            )
        )

    async def create(self, collection_name: str, domain: Metadata) -> Metadata:
        collection = self.mongo_client[collection_name]
        return await collection.insert_one(domain)
