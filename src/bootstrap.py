"""Composition root — wires concrete adapters to application ports.

All dependency construction and injection lives here. Entry points
(Flask app, CLI worker, tests) call these factories instead of
building dependencies themselves. To swap an adapter, change it here.
"""

from __future__ import annotations

from typing import Any

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.orm.scoping import scoped_session

from adapters.outgoing.persistence.repositories.observations import ObservationRepository
from adapters.outgoing.persistence.repositories.runs import RunRepository
from adapters.outgoing.persistence.repositories.targets import TargetRepository
from application.runner import Runner
from config import settings


def create_session() -> Session:
    """Create a standalone SQLAlchemy session (no Flask dependency)."""
    engine = create_engine(str(settings.database_url), pool_pre_ping=True)
    factory = sessionmaker(bind=engine)
    return factory()


def create_runner(session: Session | scoped_session[Any]) -> Runner:
    """Wire up a Runner with all concrete repositories."""
    return Runner(
        target_repo=TargetRepository(session),
        run_repo=RunRepository(session),
        obs_repo=ObservationRepository(session),
    )
