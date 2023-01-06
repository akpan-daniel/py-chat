from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "pychat_auth_authtokens" ADD "login_attempts" SMALLINT NOT NULL  DEFAULT 0;
        ALTER TABLE "pychat_auth_authtokens" ADD "last_login" TIMESTAMPTZ;
        ALTER TABLE "pychat_auth_authtokens" ALTER COLUMN "exp" DROP NOT NULL;
        ALTER TABLE "pychat_auth_authtokens" ALTER COLUMN "token" DROP NOT NULL;"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "pychat_auth_authtokens" DROP COLUMN "login_attempts";
        ALTER TABLE "pychat_auth_authtokens" DROP COLUMN "last_login";
        ALTER TABLE "pychat_auth_authtokens" ALTER COLUMN "exp" SET NOT NULL;
        ALTER TABLE "pychat_auth_authtokens" ALTER COLUMN "token" SET NOT NULL;"""
