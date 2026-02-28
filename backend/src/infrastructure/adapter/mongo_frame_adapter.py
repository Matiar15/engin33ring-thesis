import logging
import typing

from pymongo.asynchronous.collection import AsyncCollection
from pymongo.asynchronous.database import AsyncDatabase

from backend.src.frame.application.frame_port import FramePort
from backend.src.frame.domain.frame import Frame

_logger = logging.getLogger(__name__)


class MongoFrameAdapter(FramePort):
    def __init__(
        self,
        client: AsyncDatabase[typing.Mapping[str, typing.Any] | typing.Any],
    ):
        self.client: AsyncCollection[Frame] = client["frame"]

    async def create(
        self,
        frame: Frame,
    ) -> str:
        insert_one_result = await self.client.insert_one(
            frame.model_dump(
                by_alias=True,
                exclude_unset=True,
            )
        )

        return str(insert_one_result.inserted_id)
