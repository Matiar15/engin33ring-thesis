from backend.src.authentication.application.authentication_port import (
    AuthenticationPort,
)
from backend.src.hasher.application.hasher_port import HasherPort
from backend.src.user.application.user_port import UserPort


class AuthenticationAdapter(AuthenticationPort):
    def __init__(
        self,
        user_port: UserPort,
        password_hasher: HasherPort,
    ):
        self.user_port = user_port
        self.password_hasher = password_hasher

    async def authenticate(
        self,
        email: str,
        hashed_password: str,
        token: str,
    ) -> bool:
        user = await self.user_port.fetch(email, hashed_password)

        if not user:
            raise Exception("Invalid credentials.")

        if not self.password_hasher.verify(hashed_password, user.password):
            return False

        return True
