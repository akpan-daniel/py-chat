from datetime import datetime, timedelta
from logging import getLogger

import pytz
from fastapi import HTTPException, status
from tortoise.expressions import F

from pychat.config import settings
from pychat.user import services as user_service
from pychat.user.models import User
from pychat.user.schemas import input as user_input

from .models import AuthToken
from .schemas import input
from .utils import encode_token

log = getLogger(__file__)


async def signup_user(user_in: user_input.UserCreate) -> User | None:
    log.debug(f"[AUTH] signup attempt: {user_in.email}")
    user = await user_service.create_user(user_in)

    return user


async def signin_user(user_in: input.Signin) -> dict[str, User | dict]:
    log.debug(f"[AUTH] signin attempt: {user_in.email}")
    user = await user_service.get_user_or_none(email=user_in.email)

    if user is None:
        log.debug(f"[AUTH] signin notfound: {user_in.email}")
        return None

    if not user.can_login():
        log.info(f"[AUTH] signin blocked: {user.email}")
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Account is inactive"
        )

    if not user.is_password(user_in.password.get_secret_value()):
        user.login_attempts = F("login_attempts") + 1
        await user.save(update_fields=["login_attempts"])
        log.info(f"[AUTH] signin failed: {user.email}")
        return None

    if user.login_attempts > 0:
        user.login_attempts = 0
        log.debug(f"[AUTH] signin attempt-refresh: {user.email}")

    refresh_token, exp = create_refresh_token(user)
    tokens = {
        "refresh": refresh_token,
        "access": create_access_token(user),
    }

    log.debug(f"[AUTH] signin tokens generated: {user_in.email}")
    await AuthToken.update_or_create(
        defaults={"token": tokens["refresh"], "exp": exp}, user=user
    )

    log.debug(f"[AUTH] signin refresh attempt|time: {user.email}")
    user.last_login = datetime.now(tz=pytz.UTC)
    await user.save(update_fields=["last_login", "login_attempts"])

    return dict(user=user, token=tokens)


async def signin_refresh(token: str) -> dict[str, str]:
    auth_token = (
        await AuthToken.filter(token=token, exp__gt=datetime.now(tz=pytz.UTC))
        .select_related("user")
        .get_or_none()
    )
    if auth_token is None:
        return None

    access = create_access_token(auth_token.user)

    return dict(access=access, refresh=token)


def create_access_token(user: User) -> str:
    log.debug(f"[AUTH] create_access_token init: {user.email}")
    exp = datetime.now(tz=pytz.UTC) + timedelta(minutes=settings.AUTH_ACCESS_TTL)
    payload = {
        "id": user.id.hex,
        "email": user.email,
        "first_name": user.first_name,
        "last_name": user.last_name,
        "exp": exp,
    }

    return encode_token(payload)


def create_refresh_token(user: User) -> tuple[str, datetime]:
    log.debug(f"[AUTH] create_access_token init: {user.email}")
    exp = datetime.now(tz=pytz.UTC) + timedelta(minutes=settings.AUTH_REFRESH_TTL)
    payload = {
        "id": user.id.hex,
        "exp": exp,
    }

    return encode_token(payload), exp
