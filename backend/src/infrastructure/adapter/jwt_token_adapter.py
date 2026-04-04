import datetime
import logging
import typing
import opentelemetry.trace

import jwt

from backend.src.settings import Settings
from backend.src.token.application.token_port import TokenPort
from backend.src.token.api.model import Token
from backend.src.user.application.user_port import UserPort

_logger = logging.getLogger(__name__)
_tracer = opentelemetry.trace.get_tracer(__name__)


class JWTTokenAdapter(TokenPort):
    def __init__(
        self,
        settings: Settings,
        user_port: UserPort,
    ):
        self.user_port = user_port
        self.algorithm = settings.authentication.algorithm
        self.secret = settings.authentication.secret
        self.token_ttl = settings.authentication.access_token_expire_mins

    @_tracer.start_as_current_span("JWTTokenAdapter.create_token")
    async def create_token(self, user_id: str) -> Token:
        _logger.info("Creating access token for user: %s..." % user_id)
        now = datetime.datetime.now(tz=datetime.timezone.utc)
        expires_in = now + datetime.timedelta(minutes=self.token_ttl)
        access_token = {
            "sub": user_id,
            "exp": expires_in,
            "iat": now,
        }
        encoded_jwt = jwt.encode(access_token, self.secret, algorithm=self.algorithm)
        _logger.info("Access token created for user: %s" % user_id)
        return Token(access_token=encoded_jwt, token_type="bearer")

    @_tracer.start_as_current_span("JWTTokenAdapter.verify_token")
    async def verify_token(self, token: Token) -> bool:
        try:
            _logger.info("Verifying access token...")
            parsed_token = jwt.decode(
                token.access_token, self.secret, algorithms=[self.algorithm]
            )
            email = parsed_token.get("sub")
        except jwt.PyJWTError as e:
            _logger.warning("Invalid access token. Error: %s", e)
            return False

        user = self.user_port.fetch(email or "")

        if not user:
            _logger.info("User not found for access token.")
            return False

        _logger.info("Access token verified.")
        return True

    @_tracer.start_as_current_span("JWTTokenAdapter.parse_token")
    async def parse_token(self, token: Token) -> dict[str, typing.Any]:
        return jwt.decode(
            token.access_token,
            self.secret,
            algorithms=[self.algorithm],
        )
