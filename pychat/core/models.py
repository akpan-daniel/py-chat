from tortoise import fields
from tortoise.models import Model


class BaseModel(Model):
    id = fields.UUIDField(pk=True)
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)

    class Meta:
        abstract = True
        ordering = ("-created_at", "-updated_at")

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__}: {self.id}>"
