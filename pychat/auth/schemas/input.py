import pydantic

from pychat.core.schemas import ORJSONModel


class Signin(ORJSONModel):
    email: pydantic.EmailStr
    password: pydantic.SecretStr


class RefreshToken(ORJSONModel):
    refresh: str
