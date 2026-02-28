import typing
import logging

import fastapi

from contextlib import asynccontextmanager

from backend.src.analysis.application.create_analysis_use_case import CreateAnalysisUseCase
from backend.src.infrastructure.adapter.mongo_analysis_adapter import MongoAnalysisAdapter
from backend.src.infrastructure.adapter.mongo_frame_adapter import (
    MongoFrameAdapter,
)
from backend.src.infrastructure.config.logging_config import logging_config
from backend.src.frame.api.endpoints import frames_router
from backend.src.frame.application.create_frame_use_case import CreateFrameUseCase
from backend.src.infrastructure.config.mongo_config import mongo_config
from backend.src.settings import get_settings

logging_config()

_logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: fastapi.FastAPI) -> typing.AsyncGenerator[typing.Any]:
    _logger.info("Starting application...")
    settings = get_settings()
    mongo_client = mongo_config(settings)
    analysis_port = MongoAnalysisAdapter(mongo_client)
    create_frame_use_case = CreateFrameUseCase(
        frame_port=MongoFrameAdapter(mongo_client),
        analysis_port=analysis_port,
    )
    create_analysis_use_case = CreateAnalysisUseCase(
        analysis_port=analysis_port,
    )

    app.state.create_frame_use_case = create_frame_use_case
    app.state.create_analysis_use_case = create_analysis_use_case

    yield


app = fastapi.FastAPI(
    title="Engin33ring Thesis",
    lifespan=lifespan,
    debug=True,
)

app.include_router(frames_router)
