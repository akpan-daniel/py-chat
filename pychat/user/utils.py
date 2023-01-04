import re

from passlib.context import CryptContext
from pydantic import SecretStr

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def make_password(password: str) -> str:
    return pwd_context.hash(password)


def is_password(plain_password: str, hash_password: str) -> bool:
    return pwd_context.verify(plain_password, hash_password)


def is_valid_password(value: SecretStr):
    errors = []
    password = value.get_secret_value()

    if len(password) < 8:
        errors.append("Password must be at least 8 characters")
    if not re.search(r"\d", password):
        errors.append("Password must contain at least one number")
    if not (re.search("[a-z]", password) and re.search("[A-Z]", password)):
        errors.append("Password muxt contain mixed case")

    if errors:
        raise ValueError(errors)

    return value
