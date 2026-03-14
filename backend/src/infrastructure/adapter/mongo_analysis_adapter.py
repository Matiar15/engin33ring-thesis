import datetime
import logging
import typing
from typing import Any

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
        self,
        id: str,
        user_id: str,
        statuses: list[str] | None = None,
        modified_at: datetime.datetime | None = None,
    ) -> Analysis | None:
        _logger.info("Getting analysis with id: %s..." % id)

        filter_criteria = self._filters(id, user_id, statuses, modified_at)

        analysis = await self.client.find_one(filter_criteria)

        if analysis:
            _logger.info("Analysis found: %s" % analysis)

        return Analysis.model_validate(analysis)

    async def update(self, id: str, **kwargs: typing.Any) -> None:
        update_criteria = self._update_criteria(**kwargs)
        await self.client.update_one(
            filter={"_id": bson.ObjectId(id)}, update=update_criteria
        )

    async def get_one_and_update(
        self,
        id: str,
        user_id: str,
        statuses: list[str] | None = None,
        modified_at: datetime.datetime | None = None,
        **kwargs: typing.Any,
    ) -> Analysis | None:
        filter_criteria = self._filters(id, user_id, statuses, modified_at)
        update_criteria = self._update_criteria(**kwargs)
        analysis = await self.client.find_one_and_update(
            filter=filter_criteria, update=update_criteria
        )

        if not analysis:
            _logger.warning("Analysis %s not found. Skipping update." % id)
            return None

        _logger.info("Analysis updated: %s" % id)
        return Analysis.model_validate(analysis)

    @staticmethod
    def _filters(
        id: str,
        user_id: str,
        statuses: list[str] | None = None,
        modified_at: datetime.datetime | None = None,
    ) -> dict[str, typing.Any]:
        filter_criteria: dict[str, typing.Any] = {
            "_id": bson.ObjectId(id),
            "user_id": user_id,
        }

        if statuses:
            filter_criteria["status"] = {"$in": statuses}
        if modified_at:
            filter_criteria["modified_at"] = {"$lt": modified_at.isoformat()}

        return filter_criteria

    @staticmethod
    def _update_criteria(**kwargs: typing.Any) -> dict[str, typing.Any]:
        updates: dict[str, dict[typing.Any, typing.Any]] = {"$set": {}}
        updates["$set"].update({"modified_at": datetime.datetime.now().isoformat()})

        frame = kwargs.pop("frame", None)
        status = kwargs.pop("status", None)
        video_url = kwargs.pop("video_url", None)

        if frame:
            updates.update(
                {
                    "$push": {
                        "frames": frame.model_dump(by_alias=True, exclude_unset=True)
                    },
                }
            )

        if status:
            updates["$set"].update({"status": status})

        if video_url:
            updates["$set"].update({"video_url": video_url})

        return updates
