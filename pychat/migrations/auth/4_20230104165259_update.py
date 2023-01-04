from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "pychat_auth_authtokens" ALTER COLUMN "token" TYPE VARCHAR(255) USING "token"::VARCHAR(255);"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "pychat_auth_authtokens" ALTER COLUMN "token" TYPE VARCHAR(128) USING "token"::VARCHAR(128);"""
