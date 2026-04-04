import pydantic


class CreateAnalysisResponse(pydantic.BaseModel):
    id: str


def map_to_response(id: str) -> CreateAnalysisResponse:
    return CreateAnalysisResponse(id=id)


class EndAnalysisPayload(pydantic.BaseModel):
    id: str
