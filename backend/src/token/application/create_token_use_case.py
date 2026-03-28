import logging

from backend.src.hasher.application.hasher_port import HasherPort
from backend.src.token.application.token_port import TokenPort
from backend.src.token.api.model import LoginPayload
from backend.src.user.application.user_port import UserPort
from backend.src.token.api.model import Token

_logger = logging.getLogger(__name__)


class CreateTokenUseCase:
    def __init__(
        self,
        user_port: UserPort,
        password_hasher: HasherPort,
        token_port: TokenPort,
    ) -> None:
        self.user_port = user_port
        self.password_hasher = password_hasher
        self.token_port = token_port

    async def create(
        self,
        payload: LoginPayload,
    ) -> Token:
        hashed_pwd = await self.password_hasher.hash(payload.password)

        _logger.info("Fetching user with email: %s..." % payload.email)
        user = await self.user_port.fetch(
            email=payload.email,
        )
        if not user:
            raise ValueError(f"User with email: {payload.email} was not found.")

        _logger.info("Validating password...")
        if not await self.password_hasher.verify(payload.password, hashed_pwd):
            raise ValueError("Invalid password.")

        _logger.info("User found. Proceeding with token generation...")

        token = await self.token_port.create_token(user_id=user.id)

        _logger.info("Token generated.")

        return token
