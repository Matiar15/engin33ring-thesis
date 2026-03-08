import fastapi
import pydantic


class CreateAnalysisPayload(pydantic.BaseModel):
    user_id: str  # todo: retrieve this from token


class CreateAnalysisResponse(pydantic.BaseModel):
    id: str


def map_to_response(id: str) -> CreateAnalysisResponse:
    return CreateAnalysisResponse(id=id)


class EndAnalysisPayload(pydantic.BaseModel):
    id: str
    user_id: str  # todo: retrieve this from token
