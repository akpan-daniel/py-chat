from tortoise import Tortoise, fields

from pychat.config import settings
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
    last_login = fields.DatetimeField(null=True)
    login_attempts = fields.SmallIntField(default=0)
    is_active = fields.BooleanField(default=False)

    class Meta:
        table = "pychat_user_users"
        table_description = "PyChat user details"
        indexes = ("email", "username")

    def can_login(self):
        return self.is_active and self.login_attempts < settings.AUTH_MAX_LOGIN_ATTEMPTS

    def is_password(self, password: str) -> bool:
        return is_password(password, self.password)

    def make_password(self, password: str) -> None:
        # password should be validated before method call
        self.password = make_password(password)


Tortoise.init_models(["pychat.user.models"], "user")
