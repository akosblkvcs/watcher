from __future__ import annotations

from dataclasses import dataclass
from datetime import UTC, datetime

from core.db.models.watch_observation import WatchObservation
from core.db.models.watch_run import WatchRun
from core.repositories.watch_observations import WatchObservationRepository
from core.repositories.watch_runs import WatchRunRepository
from core.repositories.watch_targets import WatchTargetRepository
from core.services.diff import is_changed
from core.services.pipeline import PipelineParams, run_pipeline


@dataclass(frozen=True)
class WatcherRunResult:
    """Execution summary for a watcher run."""

    run_id: int
    targets_total: int
    targets_succeeded: int
    targets_failed: int


class WatcherRunner:
    """Orchestrates running all active watch targets and storing observations."""

    def __init__(
        self,
        target_repo: WatchTargetRepository,
        run_repo: WatchRunRepository,
        obs_repo: WatchObservationRepository,
    ) -> None:
        """Create the runner with repos."""
        self._target_repo = target_repo
        self._run_repo = run_repo
        self._obs_repo = obs_repo

    def execute(self) -> WatcherRunResult:
        """Run all active targets and persist per-target results."""
        run = WatchRun(status="partial", error_summary=None)
        self._run_repo.add(run)
        self._run_repo.flush()

        targets = self._target_repo.list_active()
        ok = 0
        fail = 0

        for t in targets:
            started = datetime.now(UTC)
            prev = t.last_processed_text

            try:
                params = PipelineParams(
                    url=t.url,
                    selector_type=t.selector_type,
                    selector=t.selector,
                    processor_type=t.processor_type,
                    processor_config=t.processor_config,
                )
                res = run_pipeline(params=params)

                finished = datetime.now(UTC)
                duration_ms = int((datetime.now(UTC) - started).total_seconds() * 1000)

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
                finished = datetime.now(UTC)
                duration_ms = int((datetime.now(UTC) - started).total_seconds() * 1000)

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

        run.finished_at = datetime.now(UTC)
        run.status = "success" if fail == 0 else "partial"
        run.error_summary = None if fail == 0 else f"{fail} targets failed"

        return WatcherRunResult(
            run_id=run.id,
            targets_total=len(targets),
            targets_succeeded=ok,
            targets_failed=fail,
        )
