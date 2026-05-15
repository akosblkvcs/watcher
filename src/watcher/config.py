# pyright: reportCallIssue=false

from __future__ import annotations

from typing import Annotated

from pydantic import Field, UrlConstraints, field_validator
from pydantic_core import MultiHostUrl
from pydantic_settings import BaseSettings, SettingsConfigDict

type PostgresPsycopgDsn = Annotated[
    MultiHostUrl,
    UrlConstraints(
        host_required=True,
        allowed_schemes=["postgresql+psycopg"],
    ),
]


class Settings(BaseSettings):
    """Application settings for the watcher service."""

    # Automatically loads from .env; ignore extra fields.
    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", extra="ignore", case_sensitive=False
    )

    database_url: PostgresPsycopgDsn

    env: str = "development"
    log_level: str = "INFO"

    http_timeout_seconds: int = Field(20, ge=1, le=300)
    http_retries: int = Field(2, ge=0, le=5)
    user_agent: str = "watcher/0.1"

    @field_validator("log_level")
    @classmethod
    def _check_log_level(cls, v: str) -> str:
        valid = {"DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"}

        if (val := v.upper()) not in valid:
            raise ValueError(f"Invalid log level. Choose from: {valid}")

        return val


settings = Settings()
