import fastapi

from analysis.application.end_analysis_use_case import EndAnalysisUseCase
from backend.src.analysis.application.create_analysis_use_case import (
    CreateAnalysisUseCase,
)
from backend.src.frame.application.create_frame_use_case import CreateFrameUseCase


def get_create_frame_use_case(request: fastapi.Request) -> CreateFrameUseCase:
    use_case: CreateFrameUseCase = request.app.state.create_frame_use_case
    return use_case


def get_create_analysis_use_case(request: fastapi.Request) -> CreateAnalysisUseCase:
    use_case: CreateAnalysisUseCase = request.app.state.create_analysis_use_case
    return use_case


def get_end_analysis_use_case(request: fastapi.Request) -> EndAnalysisUseCase:
    use_case: EndAnalysisUseCase = request.app.state.end_analysis_use_case
    return use_case
