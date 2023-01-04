import os
from enum import Enum
from functools import lru_cache
from pathlib import Path
from typing import Type

from pydantic import BaseSettings as BS

BASE_DIR = Path(__file__).parent.parent


class Env(str, Enum):
    BASE = "base"
    TEST = "test"
    PROD = "prod"


class BaseSettings(BS):
    DB_HOST: str
    DB_PORT: int
    DB_NAME: str
    DB_PASS: str
    DB_USER: str

    SECRET_KEY: str

    AUTH_ACCESS_TTL: int  # access token lifetime in minutes
    AUTH_REFRESH_TTL: int  # refresh token lifetime in minutes
    AUTH_MAX_LOGIN_ATTEMPTS: int

    STRTFORMAT: str  # str format for datetime

    class Config:
        env_file = BASE_DIR / "env/base.env"
        case_insensitive = True
        env_encoding = "utf-8"


class TestSettings(BaseSettings):
    class Config:
        env_file = BASE_DIR / "env/test.env"


class ProdSettings(BaseSettings):
    class Config:
        env_file = BASE_DIR / "env/prod.env"


@lru_cache
def get_settings() -> Type[BaseSettings]:
    match os.environ.get("APP_ENV", Env.BASE):
        case Env.PROD:
            return ProdSettings()
        case Env.TEST:
            return TestSettings()
        case _:
            return BaseSettings()


settings = get_settings()
