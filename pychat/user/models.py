from tortoise import Tortoise, fields

from pychat.core.models import HashBaseModel

from .validators import EmailValidator


class User(HashBaseModel):
    username = fields.CharField(max_length=32, null=True, unique=True)
    email = fields.CharField(
        max_length=100,
        unique=True,
        validators=[EmailValidator()],
    )
    first_name = fields.CharField(max_length=50)
    last_name = fields.CharField(max_length=50)
    password = fields.CharField(max_length=255, null=True)
    is_active = fields.BooleanField(default=False)

    class Meta:
        hash_field = "password"
        table = "pychat_user_users"
        table_description = "PyChat user details"
        indexes = ("email", "username")


Tortoise.init_models(["pychat.user.models"], "user")
