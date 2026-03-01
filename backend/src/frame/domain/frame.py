import pydantic

from datetime import datetime


class Frame(pydantic.BaseModel):
    id: str
    frame_url: str
    created_at: datetime

    model_config = {
        "populate_by_name": True,
        "extra": "forbid",
    }

    @classmethod
    def from_payload(cls, payload: dict) -> "Frame":
        return cls(**payload)
