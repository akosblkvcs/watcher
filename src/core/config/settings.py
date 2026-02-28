"""
Defines the application settings using Pydantic's BaseSettings.
"""

from __future__ import annotations

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings for the watcher service."""

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    database_url: str = ""
    env: str = "local"
    log_level: str = "INFO"
    web_port: int = 8000
    http_timeout_seconds: int = 20
    http_retries: int = 2
    user_agent: str = "watcher/0.1"
