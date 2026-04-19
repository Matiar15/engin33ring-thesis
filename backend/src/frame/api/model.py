import fastapi
import pydantic

from backend.src.frame.domain.detection import DetectionResult


class BoundingBox(pydantic.BaseModel):
    x: float
    y: float
    width: float = 100.0
    height: float = 100.0


class FrameResponse(pydantic.BaseModel):
    sign: str
    bounding_box: BoundingBox
    confidence: int = pydantic.Field(ge=0, le=100)


class FramePayload(pydantic.BaseModel):
    user_id: str
    incoming_id: str
    frame: fastapi.UploadFile
    analysis_id: str


def map_to_response(detection: DetectionResult) -> FrameResponse:
    return FrameResponse(
        sign=detection.sign_name.upper(),
        bounding_box=BoundingBox(
            x=detection.x,
            y=detection.y,
            width=detection.width,
            height=detection.height,
        ),
        confidence=int(detection.confidence * 100),
    )
