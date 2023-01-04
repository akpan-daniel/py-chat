from re import RegexFlag
from typing import Any

from tortoise.validators import RegexValidator


class EmailValidator(RegexValidator):
    def __init__(self):
        super().__init__(
            r"^(([^<>()[\]\\.,;:\s@\"]+(\.[^<>()[\]\\.,;:\s@\"]+)*)|(\".+\"))@(("
            r"\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9"
            r"\"]+\.)+[a-zA-Z]{2,}))$",
            RegexFlag.IGNORECASE,
        )

    def __call__(self, value: Any):
        try:
            super().__call__(value)
        except Exception as err:
            raise err("Invalid email supplied")
