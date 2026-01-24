import typing
import fastapi

from backend.src.dependencies import get_metadata_use_case
from backend.src.metadata.api.model import MetadataRequest
from backend.src.metadata.application.metadata_use_case import MetadataUseCase

metadata_router = fastapi.APIRouter(prefix="/metadata/")


@metadata_router.post("/")
async def create(
    payload: MetadataRequest,
    metadata_use_case: typing.Annotated[
        MetadataUseCase, fastapi.Depends(get_metadata_use_case)
    ],
):
    return metadata_use_case.create(payload)
