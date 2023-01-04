from pychat.core.schemas import ORJSONModel
from pychat.user.schemas.output import User


class Tokens(ORJSONModel):
    refresh: str
    access: str


class LoginResponse(ORJSONModel):
    token: Tokens
    user: User
