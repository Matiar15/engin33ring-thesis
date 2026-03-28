import typing
import fastapi

from backend.src.analysis.application.end_analysis_use_case import EndAnalysisUseCase
from backend.src.analysis.api.model import EndAnalysisPayload
from backend.src.analysis.application.create_analysis_use_case import (
    CreateAnalysisUseCase,
)
from backend.src.dependencies import (
    get_create_analysis_use_case,
    get_end_analysis_use_case,
)
from backend.src.infrastructure.security.get_current_user import get_current_user

analysis_router = fastapi.APIRouter(
    prefix="/analysis", dependencies=[fastapi.Depends(get_current_user)]
)


@analysis_router.post("")
async def create(
    user_id: typing.Annotated[str, fastapi.Depends(get_current_user)],
    create_analysis_use_case: typing.Annotated[
        CreateAnalysisUseCase, fastapi.Depends(get_create_analysis_use_case),
    ],
):
    return await create_analysis_use_case.create(user_id)


@analysis_router.patch("")
async def end(
    analysis_payload: EndAnalysisPayload,
    user_id: typing.Annotated[str, fastapi.Depends(get_current_user)],
    end_analysis_use_case: typing.Annotated[
        EndAnalysisUseCase, fastapi.Depends(get_end_analysis_use_case)
    ],
):
    return await end_analysis_use_case.end(analysis_payload, user_id)
