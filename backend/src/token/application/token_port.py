import abc

from backend.src.token.domain.token import Token


class TokenPort(abc.ABC):
    @abc.abstractmethod
    async def create_token(
        self,
        user_id: str,
    ) -> Token:
        """"""

    @abc.abstractmethod
    async def verify_token(
        self,
        token: Token,
    ) -> bool:
        """"""
