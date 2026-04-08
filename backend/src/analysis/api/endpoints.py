import typing
import fastapi

from backend.src.analysis.application.end_analysis_use_case import EndAnalysisUseCase
from backend.src.analysis.application.get_analysis_list_use_case import (
    GetAnalysisListUseCase,
)
from backend.src.analysis.application.get_video_url_use_case import GetVideoUrlUseCase
from backend.src.analysis.api.model import EndAnalysisPayload
from backend.src.analysis.application.create_analysis_use_case import (
    CreateAnalysisUseCase,
)
from backend.src.dependencies import (
    get_create_analysis_use_case,
    get_end_analysis_use_case,
    get_analysis_list_use_case,
    get_video_url_use_case,
)
from backend.src.infrastructure.security.get_current_user import get_current_user

analysis_router = fastapi.APIRouter(
    prefix="/analysis", dependencies=[fastapi.Depends(get_current_user)]
)


@analysis_router.post("")
async def create(
    user_id: typing.Annotated[str, fastapi.Depends(get_current_user)],
    create_analysis_use_case: typing.Annotated[
        CreateAnalysisUseCase,
        fastapi.Depends(get_create_analysis_use_case),
    ],
):
    return await create_analysis_use_case.create(user_id)


@analysis_router.get("")
async def get_list(
    user_id: typing.Annotated[str, fastapi.Depends(get_current_user)],
    get_analysis_list_use_case: typing.Annotated[
        GetAnalysisListUseCase,
        fastapi.Depends(get_analysis_list_use_case),
    ],
    limit: int = 10,
    offset: int = 0,
):
    return await get_analysis_list_use_case.get_list(user_id, limit, offset)


@analysis_router.patch("")
async def end(
    analysis_payload: EndAnalysisPayload,
    user_id: typing.Annotated[str, fastapi.Depends(get_current_user)],
    end_analysis_use_case: typing.Annotated[
        EndAnalysisUseCase, fastapi.Depends(get_end_analysis_use_case)
    ],
):
    return await end_analysis_use_case.end(analysis_payload, user_id)


@analysis_router.get("/{analysis_id}/video-url")
async def get_video_url(
    analysis_id: str,
    user_id: typing.Annotated[str, fastapi.Depends(get_current_user)],
    get_video_url_use_case: typing.Annotated[
        GetVideoUrlUseCase,
        fastapi.Depends(get_video_url_use_case),
    ],
):
    url = await get_video_url_use_case.get_url(analysis_id, user_id)
    if not url:
        raise fastapi.HTTPException(status_code=404, detail="Video URL not found.")
    return {"url": url}
