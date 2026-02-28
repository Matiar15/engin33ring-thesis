import logging
import typing

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
        self.client: AsyncCollection[Analysis] = client["analysis"]

    async def create(
            self,
            analysis: Analysis,
    ) -> str:
        _logger.info(f"Creating analysis for user: {analysis.user_id}...")
        insert_one_result = await self.client.insert_one(
            analysis.model_dump(
                by_alias=True,
                exclude_unset=True,
            )
        )

        inserted_id = str(insert_one_result.inserted_id)
        _logger.info(f"Analysis created with id: {inserted_id}")

        return inserted_id


    async def get_one(self, id: str, user_id: str) -> Analysis | None:
        _logger.info(f"Getting analysis with id: {id}...")
        analysis = await self.client.find_one({"_id": id, "user_id": user_id})

        if analysis:
            _logger.info(f"Analysis found: {analysis}")

        return analysis
