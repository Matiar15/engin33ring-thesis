import logging
import typing

from pymongo.asynchronous.collection import AsyncCollection
from pymongo.asynchronous.database import AsyncDatabase

from backend.src.user.application.user_port import UserPort
from backend.src.user.domain.user import User

_logger = logging.getLogger(__name__)

class MongoUserAdapter(UserPort):
    def __init__(
        self,
        client: AsyncDatabase[typing.Mapping[str, typing.Any] | typing.Any],
    ):
        self.client: AsyncCollection[User] = client["user"] # type: ignore

    async def create(
        self,
        user: User,
    ):
        _logger.info("Creating user...")
        insert_one_result = await self.client.insert_one(
            user.model_dump(
                by_alias=True,
                exclude_unset=True,
            ) # type: ignore
        )

        inserted_id = str(insert_one_result.inserted_id)
        _logger.info("User created with id: %s" % inserted_id)

        return inserted_id
