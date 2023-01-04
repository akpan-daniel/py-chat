from tortoise.exceptions import IntegrityError

from .models import User
from .schemas import input


async def create_user(user_in: input.UserCreate) -> User | None:
    user = User(
        email=user_in.email,
        first_name=user_in.first_name,
        last_name=user_in.last_name,
    )
    user.make_password(user_in.password.get_secret_value())
    try:
        await user.save()
    except IntegrityError:
        user = None

    return user


async def get_user_or_none(**kwargs) -> User | None:
    return await User.get_or_none(**kwargs)
