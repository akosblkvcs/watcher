"""
SQLAlchemy declarative base for all ORM models.
"""

from __future__ import annotations

from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):  # pylint: disable=too-few-public-methods
    """Declarative base type for ORM models."""
