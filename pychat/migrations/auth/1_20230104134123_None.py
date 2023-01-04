from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS "aerich" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "version" VARCHAR(255) NOT NULL,
    "app" VARCHAR(100) NOT NULL,
    "content" JSONB NOT NULL
);
CREATE TABLE IF NOT EXISTS "pychat_user_users" (
    "id" UUID NOT NULL  PRIMARY KEY,
    "created_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "username" VARCHAR(32)  UNIQUE,
    "email" VARCHAR(100) NOT NULL UNIQUE,
    "first_name" VARCHAR(50) NOT NULL,
    "last_name" VARCHAR(50) NOT NULL,
    "password" VARCHAR(255)
);
CREATE INDEX IF NOT EXISTS "idx_pychat_user_email_10ac00" ON "pychat_user_users" ("email", "username");
COMMENT ON TABLE "pychat_user_users" IS 'PyChat user details';
CREATE TABLE IF NOT EXISTS "pychat_auth_usertokens" (
    "id" UUID NOT NULL  PRIMARY KEY,
    "created_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "token" VARCHAR(128) NOT NULL,
    "is_active" BOOL NOT NULL  DEFAULT False,
    "user_id" UUID NOT NULL UNIQUE REFERENCES "pychat_user_users" ("id") ON DELETE CASCADE
);
COMMENT ON TABLE "pychat_auth_usertokens" IS 'Store authentication tokens';"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        """
