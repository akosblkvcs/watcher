from __future__ import annotations

from sqlalchemy import create_engine
from sqlalchemy.engine import Engine

from core.config.settings import settings


def build_engine() -> Engine:
    """Builds and returns a SQLAlchemy Engine instance."""
    return create_engine(settings.sqlalchemy_url, pool_pre_ping=True)
