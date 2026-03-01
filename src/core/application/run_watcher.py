"""
Executes a watcher run over all active targets and persisting results.
"""

# pylint: disable=too-few-public-methods,broad-exception-caught

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone

from core.db.models.watch_observation import WatchObservation
from core.db.models.watch_run import WatchRun
from core.repositories.watch_observations import WatchObservationRepository
from core.repositories.watch_runs import WatchRunRepository
from core.repositories.watch_targets import WatchTargetRepository
from core.services.pipeline import PipelineParams, run_pipeline
from core.services.diff import is_changed


@dataclass(frozen=True)
class RunWatcherResult:
    """Execution summary for a watcher run."""
    run_id: int
    targets_total: int
    targets_succeeded: int
    targets_failed: int


class RunWatcherUseCase:
    """
    Orchestrates running all active watch targets and storing observations.
    """

    def __init__(
        self,
        target_repo: WatchTargetRepository,
        run_repo: WatchRunRepository,
        obs_repo: WatchObservationRepository,
        *,
        user_agent: str,
        timeout_seconds: int,
    ) -> None:
        """Create the use case with repos and HTTP defaults."""
        self._target_repo = target_repo
        self._run_repo = run_repo
        self._obs_repo = obs_repo
        self._user_agent = user_agent
        self._timeout_seconds = timeout_seconds

    def execute(self) -> RunWatcherResult:
        """Run all active targets and persist per-target results."""

        run = WatchRun(status="partial", error_summary=None)
        self._run_repo.add(run)
        self._run_repo.flush()

        targets = self._target_repo.list_active()
        ok = 0
        fail = 0

        for t in targets:
            started = datetime.now(timezone.utc)
            prev = t.last_processed_text

            try:
                params = PipelineParams(
                    url=t.url,
                    selector_type=t.selector_type,
                    selector=t.selector,
                    processor_type=t.processor_type,
                    processor_config=t.processor_config,
                    user_agent=self._user_agent,
                    timeout_seconds=self._timeout_seconds,
                )
                res = run_pipeline(params=params)

                finished = datetime.now(timezone.utc)
                duration_ms = int(
                    (datetime.now(timezone.utc) - started).total_seconds()
                    * 1000
                )

                changed = is_changed(prev, res.processed_text)

                obs = WatchObservation(
                    run_id=run.id,
                    target_id=t.id,
                    raw_text=res.raw_text,
                    processed_text=res.processed_text,
                    changed=changed,
                    previous_processed_text=prev,
                    error_message=None,
                    duration_ms=duration_ms,
                )
                self._obs_repo.add(obs)

                t.last_run_at = finished
                t.last_status = "success"
                t.last_raw_text = res.raw_text
                t.last_processed_text = res.processed_text
                t.last_error_message = None
                t.last_duration_ms = duration_ms

                ok += 1

            except Exception as ex:
                finished = datetime.now(timezone.utc)
                duration_ms = int(
                    (datetime.now(timezone.utc) - started).total_seconds()
                    * 1000
                )

                obs = WatchObservation(
                    run_id=run.id,
                    target_id=t.id,
                    raw_text=None,
                    processed_text=None,
                    changed=False,
                    previous_processed_text=prev,
                    error_message=str(ex),
                    duration_ms=duration_ms,
                )
                self._obs_repo.add(obs)

                t.last_run_at = finished
                t.last_status = "failure"
                t.last_error_message = str(ex)
                t.last_duration_ms = duration_ms

                fail += 1

        run.finished_at = datetime.now(timezone.utc)
        run.status = "success" if fail == 0 else "partial"
        run.error_summary = None if fail == 0 else f"{fail} targets failed"

        return RunWatcherResult(
            run_id=run.id,
            targets_total=len(targets),
            targets_succeeded=ok,
            targets_failed=fail,
        )
