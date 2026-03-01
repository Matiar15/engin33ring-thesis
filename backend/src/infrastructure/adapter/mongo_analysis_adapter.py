import logging
import typing
import bson

from pymongo.asynchronous.collection import AsyncCollection
from pymongo.asynchronous.database import AsyncDatabase

from backend.src.analysis.application.analysis_port import AnalysisPort
from backend.src.analysis.domain.analysis import Analysis

_logger = logging.getLogger(__name__)


class MongoAnalysisAdapter(AnalysisPort):
    def __init__(
        self,
        client: AsyncDatabase[typing.Mapping[str, typing.Any] | typing.Any],
    ):
        self.client: AsyncCollection[Analysis] = client["analysis"]  # type: ignore

    async def create(
        self,
        analysis: Analysis,
    ) -> str:
        _logger.info(f"Creating analysis for user: {analysis.user_id}...")
        insert_one_result = await self.client.insert_one(
            analysis.model_dump(
                by_alias=True,
                exclude_unset=True,
            )  # type: ignore
        )

        inserted_id = str(insert_one_result.inserted_id)
        _logger.info(f"Analysis created with id: {inserted_id}")

        return inserted_id

    async def get_one(
        self, id: str, user_id: str, statuses: list[str] | None = None
    ) -> Analysis | None:
        _logger.info(f"Getting analysis with id: {id}...")

        filter_criteria: dict[str, typing.Any] = {
            "_id": bson.ObjectId(id),
            "user_id": user_id,
        }
        if statuses:
            filter_criteria["status"] = {"$in": statuses}

        analysis = await self.client.find_one(filter_criteria)

        if analysis:
            _logger.info(f"Analysis found: {analysis}")

        return Analysis.model_validate(analysis)

    async def update(self, id: str, **kwargs: typing.Any) -> None:
        updates = dict()
        frame = kwargs.pop("frame", None)
        status = kwargs.pop("status", None)

        if frame:
            updates.update(
                {
                    "$push": {
                        "frames": frame.model_dump(by_alias=True, exclude_unset=True)
                    }
                }
            )

        if status:
            updates.update({"$set": {"status": status}})

        await self.client.update_one(filter={"_id": bson.ObjectId(id)}, update=updates)
