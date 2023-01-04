import pydantic

from pychat.core.schemas import ORJSONModel

from ..utils import is_valid_password


class UserCreate(ORJSONModel):
    first_name: pydantic.constr(
        strip_whitespace=True,
        to_upper=True,
        min_length=2,
        max_length=50,
    )
    last_name: pydantic.constr(
        strip_whitespace=True,
        to_upper=True,
        min_length=2,
        max_length=50,
    )
    email: pydantic.EmailStr
    password: pydantic.SecretStr

    # validator
    _valid_password = pydantic.validator("password", allow_reuse=True)(
        is_valid_password
    )
