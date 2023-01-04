from fastapi import FastAPI
from tortoise.contrib.fastapi import register_tortoise

from pychat.database import TORTOISE_ORM
from pychat.router import api_router, router

app = FastAPI(
    title="Py Chat",
    description="A simple chat API service",
    version="0.0.1",
)

app.include_router(router)
app.include_router(api_router)

register_tortoise(
    app=app,
    config=TORTOISE_ORM,
    generate_schemas=False,
)
