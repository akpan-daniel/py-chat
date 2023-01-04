from datetime import datetime
from zoneinfo import ZoneInfo

import orjson
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel, root_validator

from pychat.config import settings


def orjson_dumps(value, *, default):
    return orjson.dumps(value, default=default).decode()


def convert_datetime_to_gmt(dt: datetime) -> str:
    if not dt.tzinfo:
        dt = dt.replace(tzinfo=ZoneInfo("UTC"))

    return dt.strftime(settings.STRTFORMAT)


class ORJSONModel(BaseModel):
    class Config:
        json_loads = orjson.loads
        json_dumps = orjson_dumps
        json_encoders = {datetime: convert_datetime_to_gmt}  # custom datetime encoder

    @root_validator()
    def set_null_microseconds(cls, data: dict) -> int:
        """Remove microseconds from all datetime field values"""
        datetime_fields = {
            key: value.replace(microsecond=0)
            for key, value in data.items()
            if isinstance(key, datetime)
        }

        return {**data, **datetime_fields}

    def serializable_dict(self, **kwargs):
        """Return a dict which contains only serializable fields"""
        default_dict = super().dict(**kwargs)

        return jsonable_encoder(default_dict)
