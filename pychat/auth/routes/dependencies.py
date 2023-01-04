from logging import getLogger

from fastapi import Header, HTTPException, status
from fastapi.security.utils import get_authorization_scheme_param

from pychat.user.models import User

from ..utils import decode_token

log = getLogger(__file__)


async def get_current_user(authorization: str | None = Header(default=None)):
    InvalidToken = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Token is invalid or expired",
    )

    _, token = get_authorization_scheme_param(authorization)
    if not token:
        log.debug("[AUTH] current_user no token")
        raise InvalidToken

    payload = decode_token(token)

    if payload is None:
        log.warn("[AUTH] current_user token invalid")
        raise InvalidToken

    payload.pop("exp")
    user = await User.get_or_none(**payload)

    if user is None:
        log.warn(f"[USER] current_user token compromised {payload.get('email')}")
        raise InvalidToken

    log.debug(f"[USER] current_user fetched: {user.email}")
    return await user
