import logging
import typing

import pymongo

from pymongo.asynchronous.database import AsyncDatabase

from backend.src.settings import Settings

_logger = logging.getLogger(__name__)


def mongo_config(
    settings: Settings,
) -> AsyncDatabase[typing.Mapping[str, typing.Any] | typing.Any]:
    connection_string = f"{settings.database.protocol}://{settings.database.user}:{settings.database.password}@{settings.database.host}/{settings.database.name}"

    _logger.info(f"Connecting to MongoDB at {settings.database.host}...")

    mongo_client = (
        pymongo.AsyncMongoClient(
            connection_string,
            maxPoolSize=20,
            maxIdleTimeMS=30_000,
            authSource="admin"
        )
    )[settings.database.name]

    _logger.info("Connected to MongoDB.")

    return mongo_client
