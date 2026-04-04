import pydantic


class UserPayload(pydantic.BaseModel):
    login: str
    password: str
    email: str
    full_name: str
