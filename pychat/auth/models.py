from tortoise import Tortoise, fields

from pychat.core.models import BaseModel


# TODO: Create table to keep track of all login attempts
class AuthToken(BaseModel):
    user = fields.OneToOneField(
        "user.User", related_name=None, on_delete=fields.CASCADE
    )
    token = fields.CharField(max_length=255)
    exp = fields.DatetimeField()

    class Meta:
        table = "pychat_auth_authtokens"
        table_description = "Store authentication tokens"


Tortoise.init_models(["pychat.auth.models"], "auth")
