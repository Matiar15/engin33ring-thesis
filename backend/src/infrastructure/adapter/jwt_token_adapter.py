import datetime
import logging

import jwt

from backend.src.settings import Settings
from backend.src.token.application.token_port import TokenPort
from backend.src.token.domain.token import Token
from backend.src.user.application.user_port import UserPort

_logger = logging.getLogger(__name__)

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

    async def create_token(self, user_id: str) -> Token:
        _logger.info("Creating access token for user: %s..." % user_id)
        expires_in = datetime.datetime.now() + datetime.timedelta(minutes=self.token_ttl)
        access_token = {
            "sub": user_id,
            "exp": expires_in,
            "iat": datetime.datetime.now(),
        }
        encoded_jwt = jwt.encode(access_token, self.secret, algorithm=self.algorithm)
        _logger.info("Access token created for user: %s" % user_id)
        return Token(access_token=encoded_jwt, token_type="bearer")

    async def verify_token(self, token: Token) -> bool:
        try:
            _logger.info("Verifying access token...")
            token = jwt.decode(token.access_token, self.secret, algorithms=[self.algorithm])
            email = token.get("sub")
        except jwt.PyJWTError:
            _logger.info("Invalid access token.")
            return False


        user = self.user_port.fetch_for_token(email)

        if not user:
            _logger.info("User not found for access token.")
            return False

        _logger.info("Access token verified.")
        return True
