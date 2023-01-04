from tortoise import Tortoise, fields

from pychat.core.models import BaseModel

from .utils import is_password, make_password
from .validators import EmailValidator


class User(BaseModel):
    username = fields.CharField(max_length=32, null=True, unique=True)
    email = fields.CharField(
        max_length=100,
        unique=True,
        validators=[EmailValidator()],
    )
    first_name = fields.CharField(max_length=50)
    last_name = fields.CharField(max_length=50)
    password = fields.CharField(max_length=255, null=True)

    class Meta:
        table = "pychat_user_users"
        table_description = "PyChat user details"
        indexes = ("email", "username")

    def is_password(self, password: str) -> bool:
        return is_password(password, self.password)

    def make_password(self, password: str) -> None:
        # password should be validated before method call
        self.password = make_password(password)


Tortoise.init_models(["pychat.user.models"], "user")
