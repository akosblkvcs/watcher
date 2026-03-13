"""Orchestrates a single watcher run across all active targets."""

from __future__ import annotations

import logging
from dataclasses import dataclass
from datetime import UTC, datetime

from application.diff import is_changed
from application.pipeline import PipelineParams, run_pipeline
from domain.enums import RunStatus, TargetStatus
from domain.events import run_completed, run_started, target_changed, target_checked
from domain.models.observation import Observation
from domain.models.run import Run
from domain.repositories import ObservationRepo, RunRepo, TargetRepo

log = logging.getLogger(__name__)


@dataclass(frozen=True)
class RunResult:
    """Execution summary for a watcher run."""

    run_id: int
    targets_total: int
    targets_succeeded: int
    targets_failed: int


class Runner:
    """Orchestrates running all active targets and storing observations."""

    def __init__(
        self,
        target_repo: TargetRepo,
        run_repo: RunRepo,
        obs_repo: ObservationRepo,
    ) -> None:
        """Create the runner with repository ports."""
        self._target_repo = target_repo
        self._run_repo = run_repo
        self._obs_repo = obs_repo

    def execute(self) -> RunResult:
        """Run all active targets and persist per-target results."""
        run = Run(status=RunStatus.PARTIAL, error_summary=None)
        self._run_repo.add(run)
        self._run_repo.flush()

        run_started.send(self, run=run)

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
                duration_ms = int((finished - started).total_seconds() * 1000)

                changed = is_changed(prev, res.processed_text)

                obs = Observation(
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
                t.last_status = TargetStatus.SUCCESS
                t.last_raw_text = res.raw_text
                t.last_processed_text = res.processed_text
                t.last_error_message = None
                t.last_duration_ms = duration_ms

                ok += 1

                target_checked.send(self, target=t, observation=obs, success=True)
                if changed:
                    target_changed.send(self, target=t, observation=obs)

            except Exception as ex:
                log.exception("Target %s (%s) failed", t.id, t.name)

                finished = datetime.now(UTC)
                duration_ms = int((finished - started).total_seconds() * 1000)

                obs = Observation(
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
                t.last_status = TargetStatus.FAILURE
                t.last_error_message = str(ex)
                t.last_duration_ms = duration_ms

                fail += 1

                target_checked.send(self, target=t, observation=obs, success=False)

        run.finished_at = datetime.now(UTC)
        run.status = RunStatus.SUCCESS if fail == 0 else RunStatus.PARTIAL
        run.error_summary = None if fail == 0 else f"{fail} targets failed"

        result = RunResult(
            run_id=run.id,
            targets_total=len(targets),
            targets_succeeded=ok,
            targets_failed=fail,
        )

        run_completed.send(self, run=run, result=result)

        return result
