"""Repository port definitions (interfaces).

These Protocol classes define the contracts that concrete repository
implementations must satisfy.  The application layer depends on these
abstractions, keeping it decoupled from any specific persistence adapter.
"""

from __future__ import annotations

from collections.abc import Sequence
from typing import Protocol

from domain.models.observation import Observation
from domain.models.run import Run
from domain.models.target import Target


class TargetRepo(Protocol):
    """Port for target persistence."""

    def list_active(self) -> Sequence[Target]:
        """Return all active targets."""
        ...

    def get(self, target_id: int) -> Target | None:
        """Return a target by id, or None if missing."""
        ...

    def add(self, target: Target) -> None:
        """Stage a target for persistence."""
        ...


class RunRepo(Protocol):
    """Port for run persistence."""

    def add(self, run: Run) -> None:
        """Stage a run for persistence."""
        ...

    def get(self, run_id: int) -> Run | None:
        """Return a run by id, or None if missing."""
        ...


class ObservationRepo(Protocol):
    """Port for observation persistence."""

    def add(self, obs: Observation) -> None:
        """Stage an observation for persistence."""
        ...

    def list_recent(self, *, limit: int) -> Sequence[Observation]:
        """Return the most recent observations (newest first)."""
        ...
