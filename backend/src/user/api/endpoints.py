import typing
import fastapi

from backend.src.dependencies import get_create_user_use_case
from backend.src.user.api.model import UserPayload
from backend.src.user.application.create_user_use_case import CreateUserUseCase

users_router = fastapi.APIRouter(prefix="/users")


@users_router.post("/")
async def create(
    payload: UserPayload,
    create_user_use_case: typing.Annotated[
        CreateUserUseCase, fastapi.Depends(get_create_user_use_case)
    ],
):
    return await create_user_use_case.create(payload)
