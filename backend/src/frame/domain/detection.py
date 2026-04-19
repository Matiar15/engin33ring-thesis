import pydantic


class DetectionResult(pydantic.BaseModel):
    sign_name: str
    confidence: float = pydantic.Field(ge=0.0, le=1.0)
    x: float
    y: float
    width: float
    height: float

