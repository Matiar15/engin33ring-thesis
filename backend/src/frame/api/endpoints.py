import typing
import fastapi

from backend.src.dependencies import get_create_frame_use_case
from backend.src.frame.api.model import FramePayload
from backend.src.frame.application.create_frame_use_case import CreateFrameUseCase

frames_router = fastapi.APIRouter(prefix="/frames")


@frames_router.post("/")
async def create(
    payload: FramePayload,
    frame_use_case: typing.Annotated[
        CreateFrameUseCase, fastapi.Depends(get_create_frame_use_case)
    ],
):
    return await frame_use_case.create(payload)
