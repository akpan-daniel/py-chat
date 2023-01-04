from logging import getLogger

from tortoise.exceptions import IntegrityError

from .models import User
from .schemas import input

log = getLogger(__file__)


async def create_user(user_in: input.UserCreate) -> User | None:
    log.debug(f"[USER] create attempt: {user_in.email}")
    user = User(
        email=user_in.email,
        first_name=user_in.first_name,
        last_name=user_in.last_name,
    )
    user.make_password(user_in.password.get_secret_value())
    try:
        await user.save()
        log.info(f"[USER] create successful: {user.email}")
    except IntegrityError:
        log.info(f"[USER] create failed: {user.email}")
        user = None

    return user


async def get_user_or_none(**kwargs) -> User | None:
    return await User.get_or_none(**kwargs)
