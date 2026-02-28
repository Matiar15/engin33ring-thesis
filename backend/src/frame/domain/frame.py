import typing

import pydantic

PyObjectId = typing.Annotated[str, pydantic.BeforeValidator(str)]


class Frame(pydantic.BaseModel):
    id: PyObjectId | None = pydantic.Field(alias="_id", default=None)
    user_id: str
    analysis_id: str
    frame_url: str

    model_config = {
        "populate_by_name": True,
        "extra": "forbid",
    }

    @classmethod
    def from_payload(cls, payload: dict) -> "Frame":
        return cls(**payload)
