from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "pychat_auth_usertokens" RENAME TO "pychat_auth_authtokens";"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "pychat_auth_authtokens" RENAME TO "pychat_auth_usertokens";"""
