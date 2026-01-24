import typing

import pydantic

PyObjectId = typing.Annotated[str, pydantic.BeforeValidator(str)]


class Metadata(pydantic.BaseModel):
    id: PyObjectId | None = pydantic.Field(alias="_id", default=None)
