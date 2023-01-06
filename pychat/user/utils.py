import re

from pydantic import SecretStr


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
