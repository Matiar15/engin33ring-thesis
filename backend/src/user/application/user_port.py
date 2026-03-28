import abc

from backend.src.user.domain.user import User


class UserPort(abc.ABC):
    @abc.abstractmethod
    async def create(
        self,
        user: User,
    ):
        """"""

    @abc.abstractmethod
    async def fetch(
        self,
        email: str,
    ) -> User | None:
        """"""
