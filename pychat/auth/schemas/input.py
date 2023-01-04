import pydantic


class Signin(pydantic.BaseModel):
    email: pydantic.EmailStr
    password: pydantic.SecretStr
