from tortoise import fields
from tortoise.models import Model

from .utils import make_hash, verifiy_hash


class BaseModel(Model):
    id = fields.UUIDField(pk=True)
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)

    class Meta:
        abstract = True
        ordering = ("-created_at", "-updated_at")

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__}: {self.id}>"


class HashBaseModel(BaseModel):
    class Meta:
        abstract = True
        hash_field = None

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        self.has_hash_attribute()

    def has_hash_attribute(self):
        field = self.Meta.hash_field
        klass = self.__class__.__name__

        if not (field and isinstance(field, str)):
            raise TypeError(f"Invalid field type {type(field)} for {klass}")
        if not hasattr(self, self.Meta.hash_field):
            raise AttributeError(
                f"{self.__class__.__name__} has no attribute {self.Meta.hash_field}"
            )

    def set_hash_field(self, value: str) -> None:
        hashed_value = make_hash(value)
        setattr(self, self.Meta.hash_field, hashed_value)

    def is_hash(self, value: str) -> bool:
        hashed_value = getattr(self, self.Meta.hash_field)
        return verifiy_hash(value, hashed_value)
