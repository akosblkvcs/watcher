"""
Provides the database engine setup.
"""

from __future__ import annotations

from sqlalchemy import create_engine
from sqlalchemy.engine import Engine


def build_engine(database_url: str) -> Engine:
    """Builds and returns a SQLAlchemy Engine instance."""

    return create_engine(database_url, pool_pre_ping=True)
