from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "pychat_user_users" DROP COLUMN "last_login";
        ALTER TABLE "pychat_user_users" DROP COLUMN "login_attempts";"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "pychat_user_users" ADD "last_login" TIMESTAMPTZ;
        ALTER TABLE "pychat_user_users" ADD "login_attempts" SMALLINT NOT NULL  DEFAULT 0;"""
