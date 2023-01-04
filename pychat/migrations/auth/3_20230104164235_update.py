from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "pychat_auth_authtokens" ADD "exp" TIMESTAMPTZ NOT NULL;
        ALTER TABLE "pychat_auth_authtokens" DROP COLUMN "is_active";"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "pychat_auth_authtokens" ADD "is_active" BOOL NOT NULL  DEFAULT False;
        ALTER TABLE "pychat_auth_authtokens" DROP COLUMN "exp";"""
