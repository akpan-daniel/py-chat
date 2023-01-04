import pydantic

from pychat.core.schemas import ORJSONModel


class User(ORJSONModel):
    id: pydantic.UUID4
    email: str
    first_name: str
    last_name: str
    username: str | None

    class Config:
        orm_mode = True
