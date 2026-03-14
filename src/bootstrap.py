"""Composition root — wires concrete adapters to application ports.

All dependency construction and injection lives here. Entry points
(Flask app, CLI worker, tests) call these factories instead of
building dependencies themselves. To swap an adapter, change it here.
"""

from __future__ import annotations

from functools import lru_cache

from sqlalchemy import Engine, create_engine
from sqlalchemy.orm import Session, sessionmaker

from adapters.outgoing.http.extractor import extract_texts_from_html
from adapters.outgoing.http.fetcher import fetch_html
from adapters.outgoing.persistence.repositories.observations import ObservationRepository
from adapters.outgoing.persistence.repositories.runs import RunRepository
from adapters.outgoing.persistence.repositories.targets import TargetRepository
from adapters.outgoing.persistence.uow import UnitOfWork
from application.pipeline import Pipeline
from application.runner import Runner
from config import settings


@lru_cache(maxsize=1)
def get_engine() -> Engine:
    """Create and cache the SQLAlchemy engine for the process."""
    return create_engine(str(settings.database_url), pool_pre_ping=True)


@lru_cache(maxsize=1)
def get_session_factory() -> sessionmaker[Session]:
    """Create and cache the SQLAlchemy session factory."""
    return sessionmaker(get_engine())


def create_session() -> Session:
    """Create a standalone SQLAlchemy session (no Flask dependency)."""
    return get_session_factory()()


def create_runner(uow: UnitOfWork) -> Runner:
    """Wire up a Runner with all concrete repositories."""
    pipeline = Pipeline(fetcher=fetch_html, extractor=extract_texts_from_html)
    return Runner(
        target_repo=TargetRepository(uow.session),
        run_repo=RunRepository(uow.session),
        obs_repo=ObservationRepository(uow.session),
        uow=uow,
        pipeline=pipeline,
    )