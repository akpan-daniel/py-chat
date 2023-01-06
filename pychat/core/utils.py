from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def make_hash(value: str) -> str:
    return pwd_context.hash(value)


def verifiy_hash(value: str, hashed_value: str) -> bool:
    return pwd_context.verify(value, hashed_value)
