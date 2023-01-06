from datetime import datetime, timedelta
from logging import getLogger

import pytz
from tortoise import transactions
from tortoise.expressions import F

from pychat.config import settings
from pychat.exceptions import PermissionDenied
from pychat.user import services as user_service
from pychat.user.models import User
from pychat.user.schemas import input as user_input

from .models import AuthToken
from .schemas import input
from .utils import encode_token

log = getLogger(__file__)


async def get_auth_token_or_none(**kwargs) -> AuthToken | None:
    return await AuthToken.filter(**kwargs).select_related("user").get_or_none(**kwargs)


async def delete_auth_token(user: User) -> None:
    await AuthToken.filter(user=user).update(token=None, exp=None)


@transactions.atomic()
async def signup_user(user_in: user_input.UserCreate) -> User | None:
    log.debug(f"[AUTH] signup attempt: {user_in.email}")
    user = await user_service.create_user(user_in)

    return user


async def signin_user(user_in: input.Signin) -> dict[str, User | dict]:
    log.debug(f"[AUTH] signin attempt: {user_in.email}")
    auth_token = await get_auth_token_or_none(user__email=user_in.email)

    if auth_token is None:
        log.debug(f"[AUTH] signin notfound: {user_in.email}")
        return None

    user: User = auth_token.user

    if not auth_token.can_login():
        log.info(f"[AUTH] signin blocked: {user.email}")
        raise PermissionDenied("Account is inactive")

    if not user.is_hash(user_in.password.get_secret_value()):
        user.login_attempts = F("login_attempts") + 1
        await user.save(update_fields=["login_attempts"])
        log.info(f"[AUTH] signin failed: {user.email}")
        return None

    auth_token.token, auth_token.exp = create_refresh_token(user)
    tokens = {
        "refresh": auth_token.token,
        "access": create_access_token(user),
    }

    log.debug(f"[AUTH] signin tokens generated: {user_in.email}")

    auth_token.login_attempts = 0
    auth_token.last_login = datetime.now(tz=pytz.UTC)
    await auth_token.save(
        update_fields=["token", "exp", "last_login", "login_attempts", "updated_at"]
    )

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
