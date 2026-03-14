import abc


class HasherPort(abc.ABC):
    @abc.abstractmethod
    async def hash(
        self,
        text: str,
    ) -> str:
        """"""

    @abc.abstractmethod
    async def verify(
        self,
        text: str,
        hashed_text: str,
    ) -> bool:
        """"""
