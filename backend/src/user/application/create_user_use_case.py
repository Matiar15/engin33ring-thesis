import logging

from backend.src.hasher.application.HasherPort import HasherPort
from backend.src.user.api.model import UserPayload
from backend.src.user.application.user_port import UserPort

_logger = logging.getLogger(__name__)

class CreateUserUseCase:
    def __init__(
        self,
        user_port: UserPort,
        password_hasher: HasherPort,
    ) -> None:
        self.user_port = user_port
        self.password_hasher = password_hasher

    async def create(
        self,
        payload: UserPayload,
    ) -> None:
        hashed_pwd = await self.password_hasher.hash(payload.password)

        try:
            _logger.info("Creating user with login: %s..." % payload.login)
            await self.user_port.create(
                login=payload.login,
                password=hashed_pwd,
                email=payload.email,
                full_name=payload.full_name,
            )
            _logger.info("User created.")

        except Exception as e:
            _logger.error("Failed to create user: %s" % e)
            raise Exception("Failed to create user. Email already exists.")