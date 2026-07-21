"""Settings for build-time collectstatic only."""

import os

_BUILD_PLACEHOLDERS = {
    "DATABASE_URL": "postgres://build:build@localhost/build",
    "SECRET_KEY": "build-only",
    "ENVIRONMENT": "production",
    "DEBUG": "False",
    "ALLOWED_HOSTS": "localhost",
    "LOG_LEVEL": "INFO",
    "HTTP_TIMEOUT_SECONDS": "20",
    "HTTP_RETRIES": "2",
    "USER_AGENT": "build",
}

for _name, _value in _BUILD_PLACEHOLDERS.items():
    os.environ.setdefault(_name, _value)

from config.settings import *  # noqa: E402, F403
