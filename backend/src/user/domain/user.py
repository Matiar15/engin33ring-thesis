import pydantic

from datetime import datetime


class User(pydantic.BaseModel):
    id: str
    login: str
    password: str
    email: str
    full_name: str
    created_at: datetime

    model_config = {
        "populate_by_name": True,
        "extra": "forbid",
    }

    @classmethod
    def from_payload(cls, payload: dict) -> "User":
        return cls(**payload)
