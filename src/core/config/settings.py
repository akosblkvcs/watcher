# pyright: reportCallIssue=false

from __future__ import annotations

from pydantic import Field, PostgresDsn, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings for the watcher service."""

    # Automatically loads from .env; ignore extra fields.
    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", extra="ignore", case_sensitive=False
    )

    database_url: PostgresDsn

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

    @property
    def sqlalchemy_url(self) -> str:
        """Fixes the 'postgres://' vs 'postgresql+psycopg://' mismatch for SQLAlchemy."""
        url = str(self.database_url)

        if url.startswith("postgres://"):
            return url.replace("postgres://", "postgresql+psycopg://", 1)
        if url.startswith("postgresql://"):
            return url.replace("postgresql://", "postgresql+psycopg://", 1)

        return url


settings = Settings()
