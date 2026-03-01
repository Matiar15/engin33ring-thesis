import typing
import fastapi

from backend.src.dependencies import get_create_frame_use_case
from backend.src.frame.api.model import FramePayload
from backend.src.frame.application.create_frame_use_case import CreateFrameUseCase

frames_router = fastapi.APIRouter(prefix="/frames")


@frames_router.post("/")
async def create(
    user_id: typing.Annotated[str, fastapi.Form(...)],
    analysis_id: typing.Annotated[str, fastapi.Form(...)],
    frame: typing.Annotated[fastapi.UploadFile, fastapi.File(...)],
    frame_use_case: typing.Annotated[
        CreateFrameUseCase, fastapi.Depends(get_create_frame_use_case)
    ],
):
    payload = FramePayload(
        user_id=user_id,
        analysis_id=analysis_id,
        frame=frame,
    )
    return await frame_use_case.create(payload)
