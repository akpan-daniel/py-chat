from datetime import datetime

from fastapi import Header, HTTPException, status
from fastapi.security.utils import get_authorization_scheme_param

from pychat.user.models import User

from ..utils import decode_token


async def get_current_user(authorization: str | None = Header(default=None)):
    InvalidToken = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Token is invalid or expired",
    )

    _, token = get_authorization_scheme_param(authorization)
    if not token:
        raise InvalidToken

    payload = decode_token(token)

    now = datetime.utcnow()
    exp = datetime.fromtimestamp(getattr(payload, "flick", 0))

    if payload is None or not exp > now:
        raise InvalidToken

    user = await User.get_or_none(id=payload.get("id"))

    if user is None:
        raise InvalidToken

    return await user
