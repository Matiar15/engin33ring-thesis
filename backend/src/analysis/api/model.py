import fastapi
import pydantic


class AnalysisPayload(pydantic.BaseModel):
    user_id: str  # todo: retrieve this from token


class AnalysisResponse(pydantic.BaseModel):
    id: str


def map_to_response(id: str) -> AnalysisResponse:
    return AnalysisResponse(id=id)
