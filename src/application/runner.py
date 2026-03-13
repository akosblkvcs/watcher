"""Orchestrates a single watcher run across all active targets."""

from __future__ import annotations

import logging
from collections.abc import Sequence
from dataclasses import dataclass
from datetime import UTC, datetime

from application.diff import is_changed
from application.pipeline import Pipeline, PipelineParams, PipelineResult
from domain.enums import RunStatus, TargetStatus
from domain.events import run_completed, run_started, target_changed, target_checked
from domain.models.observation import Observation
from domain.models.run import Run
from domain.models.target import Target
from domain.repositories import ObservationRepo, RunRepo, TargetRepo
from domain.uow import UnitOfWorkPort

log = logging.getLogger(__name__)


@dataclass(frozen=True)
class RunResult:
    """Execution summary for a watcher run."""

    run_id: int
    targets_total: int
    targets_succeeded: int
    targets_failed: int


@dataclass(frozen=True)
class TargetSuccessData:
    """Result data for a successfully processed target."""

    observation: Observation
    raw_text: str | None
    processed_text: str | None
    changed: bool
    finished: datetime
    duration_ms: int


@dataclass(frozen=True)
class TargetFailureData:
    """Result data for a failed target."""

    observation: Observation
    error_message: str
    finished: datetime
    duration_ms: int


class Runner:
    """Orchestrates running all active targets and storing observations."""

    def __init__(
        self,
        target_repo: TargetRepo,
        run_repo: RunRepo,
        obs_repo: ObservationRepo,
        uow: UnitOfWorkPort,
        pipeline: Pipeline,
    ) -> None:
        """Create the runner with repository ports."""
        self._target_repo = target_repo
        self._run_repo = run_repo
        self._obs_repo = obs_repo
        self._uow = uow
        self._pipeline = pipeline

    def execute(self) -> RunResult:
        """Run all active targets and persist per-target results."""
        run = self._create_run()
        ok = 0
        fail = 0
        targets: Sequence[Target] = []
        result: RunResult | None = None
        fatal_error: Exception | None = None

        try:
            run_started.send(self, run=run)
            targets = self._target_repo.list_active()

            for target in targets:
                if self._process_target(run, target):
                    ok += 1
                else:
                    fail += 1

            result = self._build_result(
                run_id=run.id, targets_total=len(targets), ok=ok, fail=fail
            )

            return result

        except Exception as ex:
            fatal_error = ex
            raise

        finally:
            self._finalize_run(run=run, fail=fail, fatal_error=fatal_error)

            if result is None:
                result = self._build_result(
                    run_id=run.id, targets_total=len(targets), ok=ok, fail=fail
                )

            run_completed.send(self, run=run, result=result)

    def _create_run(self) -> Run:
        """Create and persist a new run."""
        run = Run(status=RunStatus.PARTIAL, error_summary=None)
        self._run_repo.add(run)
        self._uow.flush()
        return run

    def _process_target(self, run: Run, target: Target) -> bool:
        """Process a single target. Returns True on success, else False."""
        started = datetime.now(UTC)
        previous_processed_text = target.last_processed_text

        try:
            params = PipelineParams(
                url=target.url,
                selector_type=target.selector_type,
                selector=target.selector,
                processor_type=target.processor_type,
                processor_config=target.processor_config,
            )
            pipeline_result = self._pipeline.execute(params)

            success_data = self._build_target_success_data(
                run=run,
                target=target,
                previous_processed_text=previous_processed_text,
                pipeline_result=pipeline_result,
                started=started,
            )
            self._obs_repo.add(success_data.observation)
            self._handle_target_success(target=target, data=success_data)
            return True

        except Exception as ex:
            log.exception("Target %s (%s) failed", target.id, target.name)

            failure_data = self._build_target_failure_data(
                run=run,
                target=target,
                previous_processed_text=previous_processed_text,
                error=self._format_error(ex),
                started=started,
            )
            self._obs_repo.add(failure_data.observation)
            self._handle_target_failure(target=target, data=failure_data)
            return False

    def _build_target_success_data(
        self,
        run: Run,
        target: Target,
        previous_processed_text: str | None,
        pipeline_result: PipelineResult,
        started: datetime,
    ) -> TargetSuccessData:
        """Build all success-side data for a target."""
        finished = datetime.now(UTC)
        duration_ms = self._get_duration_ms(started=started, finished=finished)
        changed = is_changed(previous_processed_text, pipeline_result.processed_text)

        observation = Observation(
            run_id=run.id,
            target_id=target.id,
            raw_text=pipeline_result.raw_text,
            processed_text=pipeline_result.processed_text,
            changed=changed,
            previous_processed_text=previous_processed_text,
            error_message=None,
            duration_ms=duration_ms,
        )

        return TargetSuccessData(
            observation=observation,
            raw_text=pipeline_result.raw_text,
            processed_text=pipeline_result.processed_text,
            changed=changed,
            finished=finished,
            duration_ms=duration_ms,
        )

    def _build_target_failure_data(
        self,
        run: Run,
        target: Target,
        previous_processed_text: str | None,
        error: str,
        started: datetime,
    ) -> TargetFailureData:
        """Build all failure-side data for a target."""
        finished = datetime.now(UTC)
        duration_ms = self._get_duration_ms(started=started, finished=finished)

        observation = Observation(
            run_id=run.id,
            target_id=target.id,
            raw_text=None,
            processed_text=None,
            changed=False,
            previous_processed_text=previous_processed_text,
            error_message=error,
            duration_ms=duration_ms,
        )

        return TargetFailureData(
            observation=observation,
            error_message=error,
            finished=finished,
            duration_ms=duration_ms,
        )

    def _handle_target_success(self, target: Target, data: TargetSuccessData) -> None:
        """Update target state and dispatch success events."""
        target.last_run_at = data.finished
        target.last_status = TargetStatus.SUCCESS
        target.last_raw_text = data.raw_text
        target.last_processed_text = data.processed_text
        target.last_error_message = None
        target.last_duration_ms = data.duration_ms

        target_checked.send(self, target=target, observation=data.observation, success=True)
        if data.changed:
            target_changed.send(self, target=target, observation=data.observation)

    def _handle_target_failure(self, target: Target, data: TargetFailureData) -> None:
        """Update target state and dispatch failure events."""
        target.last_run_at = data.finished
        target.last_status = TargetStatus.FAILURE
        target.last_error_message = data.error_message
        target.last_duration_ms = data.duration_ms

        target_checked.send(self, target=target, observation=data.observation, success=False)

    def _build_result(
        self,
        run_id: int,
        targets_total: int,
        ok: int,
        fail: int,
    ) -> RunResult:
        """Create the final run result."""
        return RunResult(
            run_id=run_id,
            targets_total=targets_total,
            targets_succeeded=ok,
            targets_failed=fail,
        )

    def _finalize_run(
        self,
        run: Run,
        fail: int,
        fatal_error: Exception | None,
    ) -> None:
        """Mark the run as finished with its final status."""
        run.finished_at = datetime.now(UTC)

        if fatal_error is not None:
            run.status = RunStatus.FAILURE
            run.error_summary = self._format_error(fatal_error)
            return

        run.status = RunStatus.SUCCESS if fail == 0 else RunStatus.PARTIAL
        run.error_summary = None if fail == 0 else f"{fail} targets failed"

    def _get_duration_ms(self, started: datetime, finished: datetime) -> int:
        """Convert elapsed time to milliseconds."""
        return int((finished - started).total_seconds() * 1000)

    def _format_error(self, ex: Exception) -> str:
        """Format an exception for persistence."""
        return f"{type(ex).__name__}: {ex}"
