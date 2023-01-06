from typing import Any, Type

from tortoise import Tortoise, fields
from tortoise.signals import post_save

from pychat.config import settings
from pychat.core.models import BaseModel
from pychat.user.models import User


# TODO: Create table to keep track of all login attempts
class AuthToken(BaseModel):
    user = fields.OneToOneField(
        "user.User", related_name=None, on_delete=fields.CASCADE
    )
    login_attempts = fields.SmallIntField(default=0)
    last_login = fields.DatetimeField(null=True)
    token = fields.CharField(max_length=255, null=True)
    exp = fields.DatetimeField(null=True)

    class Meta:
        table = "pychat_auth_authtokens"
        table_description = "Store authentication tokens"

    def can_login(self):
        login_attempts = self.login_attempts < settings.AUTH_MAX_LOGIN_ATTEMPTS
        return self.user.is_active and login_attempts


@post_save(User)
async def create_auth_token(
    sender: "Type[User]", instance: User, created: bool, **kwargs: dict[str, Any]
) -> None:
    if created:
        await AuthToken.create(user=instance)


Tortoise.init_models(["pychat.auth.models"], "auth")
