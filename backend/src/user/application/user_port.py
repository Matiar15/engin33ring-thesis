import abc

from backend.src.user.domain.user import User


class UserPort(abc.ABC):
    @abc.abstractmethod
    async def create(
        self,
        user: User,
    ):
        """"""
