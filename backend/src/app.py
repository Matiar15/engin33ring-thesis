import typing
import logging

import fastapi

from contextlib import asynccontextmanager

from fastapi.middleware.cors import CORSMiddleware

from backend.src.analysis.application.end_analysis_use_case import EndAnalysisUseCase
from backend.src.analysis.api.endpoints import analysis_router
from backend.src.analysis.application.create_analysis_use_case import (
    CreateAnalysisUseCase,
)
from backend.src.infrastructure.adapter.hasher_adapter import HasherAdapter
from backend.src.infrastructure.adapter.jwt_token_adapter import JWTTokenAdapter
from backend.src.infrastructure.adapter.mongo_user_adapter import MongoUserAdapter
from backend.src.infrastructure.adapter.rustfs_long_term_storage_adapter import (
    RustFSLongTermStorageAdapter,
)
from backend.src.infrastructure.adapter.mongo_analysis_adapter import (
    MongoAnalysisAdapter,
)
from backend.src.infrastructure.adapter.ffmpeg_stitcher_adapter import (
    FFMpegStitcherAdapter,
)
from backend.src.infrastructure.config.logging_config import logging_config
from backend.src.infrastructure.config.tracing_config import tracing_config
from backend.src.frame.api.endpoints import frames_router
from backend.src.frame.application.create_frame_use_case import CreateFrameUseCase
from backend.src.infrastructure.config.mongo_config import mongo_config
from backend.src.infrastructure.config.rustfs_config import rustfs_config
from backend.src.settings import get_settings
from prometheus_fastapi_instrumentator import Instrumentator
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor

from backend.src.token.api.endpoints import tokens_router
from backend.src.token.application.create_token_use_case import CreateTokenUseCase
from backend.src.user.api.endpoints import users_router
from backend.src.user.application.create_user_use_case import CreateUserUseCase

logging_config()
tracing_config()

_logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: fastapi.FastAPI) -> typing.AsyncGenerator[typing.Any]:
    _logger.info("Starting application...")
    settings = get_settings()

    mongo_client = await mongo_config(settings)
    long_term_storage_client = rustfs_config(settings)
    _logger.info("Initialized database ports.")

    analysis_port = MongoAnalysisAdapter(mongo_client)
    _logger.info("Initialized analysis port.")

    long_term_storage_port = RustFSLongTermStorageAdapter(long_term_storage_client)
    _logger.info("Initialized long term storage port.")

    stitcher_port = FFMpegStitcherAdapter(
        long_term_storage_port,
        settings,
    )
    _logger.info("Initialized stitcher port.")

    user_adapter = MongoUserAdapter(mongo_client)
    _logger.info("Initialized user port.")

    hasher_port = HasherAdapter()
    _logger.info("Initialized hasher port.")

    token_port = JWTTokenAdapter(
        settings=settings,
        user_port=user_adapter,
    )
    _logger.info("Initialized token port.")

    create_frame_use_case = CreateFrameUseCase(
        analysis_port=analysis_port,
        long_term_storage_port=long_term_storage_port,
    )
    create_analysis_use_case = CreateAnalysisUseCase(
        analysis_port=analysis_port,
    )
    end_analysis_use_case = EndAnalysisUseCase(
        analysis_port=analysis_port,
        stitcher_port=stitcher_port,
    )
    create_user_use_case = CreateUserUseCase(
        user_port=user_adapter,
        password_hasher=hasher_port,
    )
    create_token_use_case = CreateTokenUseCase(
        user_port=user_adapter,
        password_hasher=hasher_port,
        token_port=token_port,
    )
    _logger.info("Initialized use cases.")

    app.state.create_frame_use_case = create_frame_use_case
    app.state.create_analysis_use_case = create_analysis_use_case
    app.state.end_analysis_use_case = end_analysis_use_case
    app.state.create_user_use_case = create_user_use_case
    app.state.create_token_use_case = create_token_use_case
    app.state.token_port = token_port

    _logger.info("Application started.")
    yield
    _logger.info("Stopping application...")


from fastapi import Request
from fastapi.responses import JSONResponse
from pydantic import ValidationError

app = fastapi.FastAPI(
    title="Engin33ring Thesis",
    lifespan=lifespan,
    debug=True,
)


@app.exception_handler(ValidationError)
async def pydantic_validation_exception_handler(request: Request, exc: ValidationError):
    return JSONResponse(
        status_code=400,
        content={"detail": exc.errors(), "message": "Validation error"},
    )


@app.exception_handler(ValueError)
async def in_app_error_exception_handler(request: Request, exc: ValueError):
    return JSONResponse(
        status_code=400,
        content={"detail": exc.args, "message": "Application error occurred"},
    )


app.add_middleware(
    CORSMiddleware,
    allow_origin_regex="http://.*",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*", "traceparent", "tracestate"],
    expose_headers=["*", "traceparent", "tracestate"],
)

app.include_router(frames_router)
app.include_router(analysis_router)
app.include_router(users_router)
app.include_router(tokens_router)

Instrumentator().instrument(app).expose(app)
FastAPIInstrumentor.instrument_app(app)
