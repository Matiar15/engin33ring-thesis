import typing
import logging

import fastapi

from contextlib import asynccontextmanager

from fastapi import FastAPI

from backend.src.infrastructure.adapter.mongo_database_adapter import (
    MetadataMongoDatabaseAdapter,
)
from backend.src.infrastructure.config.logging_config import logging_config
from backend.src.metadata.application.metadata_use_case import MetadataUseCase
from backend.src.settings import get_settings

logging_config()

_logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: fastapi.FastAPI) -> typing.AsyncGenerator[typing.Any]:
    _logger.info("Starting application...")
    settings = get_settings()
    metadata_use_case = MetadataUseCase(
        database_port=MetadataMongoDatabaseAdapter(settings),
    )
    app.state.metadata_use_case = metadata_use_case
    yield


app = FastAPI(
    title="Engin33ring Thesis",
    lifespan=lifespan,
    debug=True,
)
