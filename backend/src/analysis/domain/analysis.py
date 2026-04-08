import datetime
import typing

import pydantic

from backend.src.frame.domain.frame import Frame

PyObjectId = typing.Annotated[str, pydantic.BeforeValidator(str)]


class Analysis(pydantic.BaseModel):
    id: PyObjectId | None = pydantic.Field(alias="_id", default=None)
    user_id: str
    status: str
    modified_at: datetime.datetime
    frames: list[Frame] | None = None
    video_url: str | None = None

    model_config = {
        "populate_by_name": True,
        "extra": "forbid",
    }

    @classmethod
    def from_payload(cls, payload: dict) -> "Analysis":
        return cls(**payload)
