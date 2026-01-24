import typing

import pymongo

from backend.src.infrastructure.port.database_port import DatabasePort

T = typing.TypeVar("T")


class MongoDatabaseAdapter(DatabasePort[T], typing.Generic[T]):
    def __init__(self, mongo_client: pymongo.AsyncMongoClient[T]):
        self.mongo_client = mongo_client


    async def create(self, collection_name: str, domain: T) -> T:
        collection = self.mongo_client[collection_name]
        return await collection.insert_one(domain)

