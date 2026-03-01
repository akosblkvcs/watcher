from __future__ import annotations

from sqlalchemy.orm import sessionmaker

from core.db.engine import build_engine


def build_session_maker():
    """Builds a SQLAlchemy session maker for the given database URL."""
    engine = build_engine()

    return sessionmaker(bind=engine, autoflush=False, autocommit=False, expire_on_commit=False)
