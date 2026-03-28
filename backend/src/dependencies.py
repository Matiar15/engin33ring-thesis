import fastapi

from backend.src.analysis.application.end_analysis_use_case import EndAnalysisUseCase
from backend.src.analysis.application.create_analysis_use_case import (
    CreateAnalysisUseCase,
)
from backend.src.frame.application.create_frame_use_case import CreateFrameUseCase
from backend.src.token.application.create_token_use_case import CreateTokenUseCase
from backend.src.token.application.token_port import TokenPort
from backend.src.user.application.create_user_use_case import CreateUserUseCase


def get_create_frame_use_case(request: fastapi.Request) -> CreateFrameUseCase:
    use_case: CreateFrameUseCase = request.app.state.create_frame_use_case
    return use_case


def get_create_analysis_use_case(request: fastapi.Request) -> CreateAnalysisUseCase:
    use_case: CreateAnalysisUseCase = request.app.state.create_analysis_use_case
    return use_case


def get_end_analysis_use_case(request: fastapi.Request) -> EndAnalysisUseCase:
    use_case: EndAnalysisUseCase = request.app.state.end_analysis_use_case
    return use_case


def get_create_user_use_case(request: fastapi.Request) -> CreateUserUseCase:
    use_case: CreateUserUseCase = request.app.state.create_user_use_case
    return use_case


def get_create_token_use_case(request: fastapi.Request) -> CreateTokenUseCase:
    use_case: CreateTokenUseCase = request.app.state.create_token_use_case
    return use_case


def get_token_port(request: fastapi.Request) -> TokenPort:
    port: TokenPort = request.app.state.token_port
    return port
