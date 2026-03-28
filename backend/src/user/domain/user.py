import pydantic
import datetime

from backend.src.analysis.domain.analysis import PyObjectId


class User(pydantic.BaseModel):
    id: PyObjectId | None = pydantic.Field(alias="_id", default=None)
    login: str
    password: str
    email: str
    full_name: str
    created_at: datetime.datetime
    modified_at: datetime.datetime

    model_config = {
        "populate_by_name": True,
        "extra": "forbid",
    }

    @classmethod
    def from_payload(cls, payload: dict) -> "User":
        return cls(**payload)
