import typing

import pydantic

PyObjectId = typing.Annotated[str, pydantic.BeforeValidator(str)]


class Analysis(pydantic.BaseModel):
    id: PyObjectId | None = pydantic.Field(alias="_id", default=None)
    user_id: str

    model_config = {
        "populate_by_name": True,
        "extra": "forbid",
    }

    @classmethod
    def from_payload(cls, payload: dict) -> "Analysis":
        return cls(**payload)
