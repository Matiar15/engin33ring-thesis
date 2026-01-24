import pymongo

from backend.src.infrastructure.port.database_port import DatabasePort
from backend.src.infrastructure.adapter.mongo_database_adapter import MongoDatabaseAdapter
from backend.src.settings import Settings


async def database_config(settings: Settings) -> DatabasePort:
    connection_string = f"mongodb+srv://{settings.database.user}:{settings.database.password}@{settings.database.host}/{settings.database.name}"

    client = pymongo.AsyncMongoClient(
        connection_string,
        maxPoolSize=20,
        maxIdleTimeMS=30_000,
    )

    return MongoDatabaseAdapter(mongo_client=client)