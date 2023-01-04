from jose import JWTError, jwt

from pychat.config import settings

SECRET_KEY = settings.SECRET_KEY
ALGORITHM = "HS256"


def encode_token(data: dict) -> str:
    return jwt.encode(data, SECRET_KEY, ALGORITHM)


def decode_token(token: str) -> dict | None:
    try:
        return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except JWTError:
        return None
