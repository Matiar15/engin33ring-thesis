import typing
import fastapi

from backend.src.analysis.api.model import AnalysisPayload
from backend.src.analysis.application.create_analysis_use_case import (
    CreateAnalysisUseCase,
)
from backend.src.dependencies import get_create_analysis_use_case

analysis_router = fastapi.APIRouter(prefix="/analysis")


@analysis_router.post("/")
async def create(
    analysis_payload: AnalysisPayload,
    create_analysis_use_case: typing.Annotated[
        CreateAnalysisUseCase, fastapi.Depends(get_create_analysis_use_case)
    ],
):
    return await create_analysis_use_case.create(analysis_payload)
