#!/usr/bin/env python

import os
import sys

from pychat.config import settings

TORTOISE_ORM = {
    "connections": {
        "default": {
            "engine": "tortoise.backends.asyncpg",
            "credentials": {
                "host": settings.DB_HOST,
                "port": settings.DB_PORT,
                "user": settings.DB_USER,
                "password": settings.DB_PASS,
                "database": settings.DB_NAME,
            },
        },
        # "default": "postgres://user:pass@host:port/name"
    },
    "apps": {
        "user": {
            "models": [
                "aerich.models",
                "pychat.user.models",
            ],
            # "default_connection": "default" # specify connection to use
        },
        "auth": {
            "models": [
                "pychat.auth.models",
            ],
        },
    },
    "use_tz": True,
    "timezone": "UTC",
}

apps = TORTOISE_ORM.get("apps", {})


if __name__ == "__main__":
    arg = sys.argv[1]

    match arg:
        case "upgrade":
            cmd = "upgrade"
        case "downgrade":
            cmd = "downgrade"
        case "init":
            cmd = "init-db"
        case "makemigrations":
            cmd = "migrate"
        case _:
            print(
                f"Unknown argument {arg}\nSupported args: "
                "`upgrade` `downgrade` `init` `makemigrations`"
            )
            sys.exit(1)

    size = os.get_terminal_size()
    for app in apps:
        print(f"{app}".center(size.columns, "-"))
        result = os.system(f"aerich --app {app} {cmd}")  # noqa: S605
        if result != 0:
            print(f"Error running {cmd} on {app}")
