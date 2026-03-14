import abc

class AuthenticationPort(abc.ABC):
    @abc.abstractmethod
    async def authenticate(
        self,
        email: str,
        password: str,
        token: str,
    ) -> bool:
        """"""
