import abc
import datetime
import typing

from backend.src.analysis.domain.analysis import Analysis


class AnalysisPort(abc.ABC):
    @abc.abstractmethod
    async def create(
        self,
        analysis: Analysis,
    ) -> str:
        """"""

    @abc.abstractmethod
    async def get_one(
        self,
        id: str,
        user_id: str,
        statuses: list[str] | None = None,
        modified_at: datetime.datetime | None = None,
    ) -> Analysis | None:
        """"""

    @abc.abstractmethod
    async def update(self, id: str, **kwargs: typing.Any) -> None:
        """"""

    @abc.abstractmethod
    async def get_one_and_update(
        self,
        id: str,
        user_id: str,
        statuses: list[str] | None = None,
        modified_at: datetime.datetime | None = None,
        **kwargs: typing.Any,
    ) -> Analysis | None:
        """"""

    @abc.abstractmethod
    async def get_list(
        self,
        user_id: str,
        limit: int = 10,
        offset: int = 0,
    ) -> list[Analysis]:
        """"""
