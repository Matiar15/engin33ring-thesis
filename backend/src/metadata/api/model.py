import pydantic

from backend.src.metadata.domain.metadata import Metadata


class MetadataResponse(pydantic.BaseModel):
    id: str


class MetadataRequest(pydantic.BaseModel):
    name: str


def map_to_response(metadata: Metadata) -> MetadataResponse:
    return MetadataResponse(id=metadata.id)
