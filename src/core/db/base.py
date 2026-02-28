"""
SQLAlchemy declarative base for all ORM models.
"""

# pylint: disable=too-few-public-methods

from __future__ import annotations

from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    """Declarative base type for ORM models."""
