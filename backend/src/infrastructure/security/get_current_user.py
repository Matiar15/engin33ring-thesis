import logging

import fastapi
from fastapi.security import OAuth2PasswordBearer

from backend.src.dependencies import get_token_port
from backend.src.token.application.token_port import TokenPort
from backend.src.token.api.model import Token

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/tokens")

_logger = logging.getLogger(__name__)


async def get_current_user(
    token: str = fastapi.Depends(oauth2_scheme),
    token_port: TokenPort = fastapi.Depends(get_token_port),
) -> str:
    _logger.info("Getting current user...")
    token_payload = Token(access_token=token, token_type="bearer")

    is_authorized = await token_port.verify_token(token_payload)

    if not is_authorized:
        _logger.warning("Invalid credentials. User not authorized.")
        raise fastapi.HTTPException(
            status_code=fastapi.status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
        )

    _logger.info("User authorized. Retrieving user ID...")
    user = (await token_port.parse_token(token_payload)).get("sub")

    if not user:
        _logger.warning("User ID not found in token. Token malformed.")
        raise fastapi.HTTPException(
            status_code=fastapi.status.HTTP_401_UNAUTHORIZED,
        )

    _logger.info("User ID retrieved: %s" % user)
    return user
