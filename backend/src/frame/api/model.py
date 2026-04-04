import fastapi
import pydantic


class BoundingBox(pydantic.BaseModel):
    x: float
    y: float
    width: float = 100.0
    height: float = 100.0


class FrameResponse(pydantic.BaseModel):
    sign: str
    bounding_box: BoundingBox


class FramePayload(pydantic.BaseModel):
    user_id: str  # todo: retrieve this from token
    incoming_id: str
    frame: fastapi.UploadFile
    analysis_id: str


def map_to_response() -> FrameResponse:
    return FrameResponse(
        sign="SPEED_LIMIT_30",
        bounding_box=BoundingBox(x=100, y=64, width=120, height=120),
    )
