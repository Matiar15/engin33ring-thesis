import typing
import fastapi

from backend.src.dependencies import get_create_token_use_case
from backend.src.token.api.model import LoginPayload
from backend.src.token.application.create_token_use_case import CreateTokenUseCase

token_router = fastapi.APIRouter(prefix="/tokens")


@token_router.post("/")
async def create(
    payload: LoginPayload,
    create_token_use_case: typing.Annotated[
        CreateTokenUseCase, fastapi.Depends(get_create_token_use_case)
    ],
):
    return await create_token_use_case.create(payload)
