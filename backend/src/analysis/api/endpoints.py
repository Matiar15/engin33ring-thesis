import typing
import fastapi

from backend.src.analysis.application.end_analysis_use_case import EndAnalysisUseCase
from backend.src.analysis.api.model import CreateAnalysisPayload, EndAnalysisPayload
from backend.src.analysis.application.create_analysis_use_case import (
    CreateAnalysisUseCase,
)
from backend.src.dependencies import (
    get_create_analysis_use_case,
    get_end_analysis_use_case,
)

analysis_router = fastapi.APIRouter(prefix="/analysis")


@analysis_router.post("/")
async def create(
    analysis_payload: CreateAnalysisPayload,
    create_analysis_use_case: typing.Annotated[
        CreateAnalysisUseCase, fastapi.Depends(get_create_analysis_use_case)
    ],
):
    return await create_analysis_use_case.create(analysis_payload)


@analysis_router.patch("/")
async def end(
    analysis_payload: EndAnalysisPayload,
    end_analysis_use_case: typing.Annotated[
        EndAnalysisUseCase, fastapi.Depends(get_end_analysis_use_case)
    ],
):
    return await end_analysis_use_case.end(analysis_payload)
