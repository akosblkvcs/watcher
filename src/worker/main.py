"""
Provides the main entry point for the watcher worker service.
"""

from __future__ import annotations

from core.application.run_watcher import RunWatcherUseCase
from core.config.settings import Settings
from core.db.session import build_session_maker
from core.db.uow import UnitOfWork
from core.repositories.watch_observations import WatchObservationRepository
from core.repositories.watch_runs import WatchRunRepository
from core.repositories.watch_targets import WatchTargetRepository


def main() -> int:
    """Main entry point for the watcher worker service."""

    settings = Settings()
    settings.validate_required()

    session_maker = build_session_maker(settings.database_url)

    with UnitOfWork(session_maker) as uow:
        assert uow.session is not None

        target_repo = WatchTargetRepository(uow.session)
        run_repo = WatchRunRepository(uow.session)
        obs_repo = WatchObservationRepository(uow.session)

        use_case = RunWatcherUseCase(
            target_repo,
            run_repo,
            obs_repo,
            user_agent=settings.user_agent,
            timeout_seconds=settings.http_timeout_seconds,
        )

        result = use_case.execute()

    print(
        "run_id="
        f"{result.run_id} total={result.targets_total} "
        f"ok={result.targets_succeeded} fail={result.targets_failed}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
