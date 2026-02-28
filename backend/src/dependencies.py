import fastapi

from backend.src.analysis.application.create_analysis_use_case import (
    CreateAnalysisUseCase,
)
from backend.src.frame.application.frame_use_case import CreateFrameUseCase


def get_create_frame_use_case(request: fastapi.Request) -> CreateFrameUseCase:
    use_case: CreateFrameUseCase = request.app.state.create_frame_use_case
    return use_case


def get_create_analysis_use_case(request: fastapi.Request) -> CreateAnalysisUseCase:
    use_case: CreateAnalysisUseCase = request.app.state.create_analysis_use_case
    return use_case
