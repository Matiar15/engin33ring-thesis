import pydantic



class MetadataResponse(pydantic.BaseModel):
    inserted_id: str


class MetadataRequest(pydantic.BaseModel):
    name: str


def map_to_response(inserted_id: str) -> MetadataResponse:
    return MetadataResponse(inserted_id=str(inserted_id))
