import abc

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
    ) -> Analysis | None:
        """"""
