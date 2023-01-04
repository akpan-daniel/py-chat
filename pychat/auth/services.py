from datetime import datetime, timedelta

from pychat.config import settings
from pychat.user import services as user_service
from pychat.user.models import User
from pychat.user.schemas import input as user_input

from .models import AuthToken
from .schemas import input
from .utils import encode_token


async def signup_user(user_in: user_input.UserCreate) -> User | None:
    user = await user_service.create_user(user_in)
    return user


async def signin_user(user_in: input.Signin) -> dict[str, User | dict]:
    user = await user_service.get_user_or_none(email=user_in.email)
    if user is None or not user.is_password(user_in.password.get_secret_value()):
        return None

    refresh_token, exp = create_refresh_token(user)
    tokens = {
        "refresh": refresh_token,
        "access": create_access_token(user),
    }

    print(tokens)

    await AuthToken.update_or_create(
        defaults={"token": tokens["refresh"], "exp": exp}, user=user
    )

    return dict(user=user, token=tokens)


def create_access_token(user: User) -> str:
    exp = datetime.utcnow() + timedelta(minutes=settings.AUTH_ACCESS_TTL)
    payload = {
        "id": user.id.hex,
        "email": user.email,
        "first_name": user.first_name,
        "last_name": user.last_name,
        "exp": exp,
    }

    return encode_token(payload)


def create_refresh_token(user: User) -> tuple[str, datetime]:
    exp = datetime.utcnow() + timedelta(minutes=settings.AUTH_REFRESH_TTL)
    payload = {
        "id": user.id.hex,
        "exp": exp,
    }

    return encode_token(payload), exp
