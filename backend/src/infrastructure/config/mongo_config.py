import logging
import typing
from typing import Any, Mapping

import pymongo

from pymongo.asynchronous.database import AsyncDatabase

from backend.src.settings import Settings

_logger = logging.getLogger(__name__)


async def mongo_config(
    settings: Settings,
) -> AsyncDatabase[typing.Mapping[str, typing.Any] | typing.Any]:
    connection_string = f"{settings.database.protocol}://{settings.database.user}:{settings.database.password}@{settings.database.host}/{settings.database.name}"

    _logger.info(f"Connecting to MongoDB at {settings.database.host}...")

    mongo_client: AsyncDatabase[Mapping[str, Any] | Any] = (
        pymongo.AsyncMongoClient(
            connection_string,
            maxPoolSize=20,
            maxIdleTimeMS=30_000,
            authSource="admin",
        )
    )[settings.database.name]

    _logger.info("Connected to MongoDB.")

    await _migrations(mongo_client)

    return mongo_client


async def _migrations(
    client: AsyncDatabase[typing.Mapping[str, typing.Any] | typing.Any],
) -> None:
    _logger.info("Running migrations...")
    collections = [
        "analysis",
        "user",
    ]
    existing_collections = await client.list_collection_names()

    for collection in collections:
        if collection not in existing_collections:
            _logger.info("Creating collection: %s" % collection)
            await client.create_collection(collection)

    _logger.info("Creating indexes...")
    await client.user.create_index("email", unique=True)

    _logger.info("Migrations completed.")
