"""
Database session factory.
"""

from __future__ import annotations

from sqlalchemy.orm import sessionmaker

from core.db.engine import build_engine


def build_session_factory(database_url: str):
    """Builds a SQLAlchemy session factory for the given database URL."""

    engine = build_engine(database_url)

    return sessionmaker(
        bind=engine,
        autoflush=False,
        autocommit=False,
        expire_on_commit=False
    )
