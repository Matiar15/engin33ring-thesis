import pydantic

from datetime import datetime


class Frame(pydantic.BaseModel):
    id: str
    frame_url: str
    created_at: datetime
    sign: str | None = None
    x: float | None = None
    y: float | None = None
    width: float | None = None
    height: float | None = None

    model_config = {
        "populate_by_name": True,
        "extra": "forbid",
    }

    @classmethod
    def from_payload(cls, payload: dict) -> "Frame":
        return cls(**payload)
