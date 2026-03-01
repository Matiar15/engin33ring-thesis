import typing
import logging

import fastapi

from contextlib import asynccontextmanager

from backend.src.analysis.api.endpoints import analysis_router
from backend.src.analysis.application.create_analysis_use_case import (
    CreateAnalysisUseCase,
)
from backend.src.infrastructure.adapter.rustfs_long_term_storage_adapter import (
    RustFSLongTermStorageAdapter,
)
from backend.src.infrastructure.adapter.mongo_analysis_adapter import (
    MongoAnalysisAdapter,
)
from backend.src.infrastructure.config.logging_config import logging_config
from backend.src.frame.api.endpoints import frames_router
from backend.src.frame.application.create_frame_use_case import CreateFrameUseCase
from backend.src.infrastructure.config.mongo_config import mongo_config
from backend.src.infrastructure.config.rustfs_config import rustfs_config
from backend.src.settings import get_settings

logging_config()

_logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: fastapi.FastAPI) -> typing.AsyncGenerator[typing.Any]:
    _logger.info("Starting application...")
    settings = get_settings()

    mongo_client = mongo_config(settings)
    long_term_storage_client = rustfs_config(settings)
    _logger.info("Initialized database ports.")

    analysis_port = MongoAnalysisAdapter(mongo_client)
    _logger.info("Initialized analysis port.")

    long_term_storage_port = RustFSLongTermStorageAdapter(long_term_storage_client)
    _logger.info("Initialized long term storage port.")

    create_frame_use_case = CreateFrameUseCase(
        analysis_port=analysis_port,
        long_term_storage_port=long_term_storage_port,
    )
    create_analysis_use_case = CreateAnalysisUseCase(
        analysis_port=analysis_port,
    )
    _logger.info("Initialized use cases.")

    app.state.create_frame_use_case = create_frame_use_case
    app.state.create_analysis_use_case = create_analysis_use_case

    _logger.info("Initialized application.")
    yield
    _logger.info("Stopping application...")


app = fastapi.FastAPI(
    title="Engin33ring Thesis",
    lifespan=lifespan,
    debug=True,
)

app.include_router(frames_router)
app.include_router(analysis_router)
