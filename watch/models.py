"""Domain models: a Target is watched; each Run produces Observations."""

from datetime import datetime
from typing import Any

from django.db import models


class Target(models.Model):
    """A web page to watch for changes."""

    class SelectorType(models.TextChoices):
        CSS = "css", "CSS"
        XPATH = "xpath", "XPath"

    class ProcessorType(models.TextChoices):
        RAW_TEXT = "raw_text", "Raw text"
        MIN_VALUE = "min_value", "Minimum value"

    class Status(models.TextChoices):
        SUCCESS = "success", "Success"
        FAILURE = "failure", "Failure"

    class FetchMethod(models.TextChoices):
        HTTPX = "httpx", "HTTPX"
        BRIGHTDATA = "brightdata", "Bright Data"

    name: models.CharField[str, str] = models.CharField(max_length=200)
    url: models.URLField[str, str] = models.URLField(max_length=2000)

    selector_type: models.CharField[str, str] = models.CharField(
        max_length=10,
        choices=SelectorType.choices,
        default=SelectorType.CSS,
    )
    selector: models.TextField[str, str] = models.TextField()

    processor_type: models.CharField[str, str] = models.CharField(
        max_length=50,
        choices=ProcessorType.choices,
        default=ProcessorType.RAW_TEXT,
    )
    processor_config: models.JSONField[dict[str, Any] | None, dict[str, Any] | None] = (
        models.JSONField(null=True, blank=True)
    )

    fetch_method: models.CharField[str, str] = models.CharField(
        max_length=50,
        choices=FetchMethod.choices,
        default=FetchMethod.HTTPX,
    )

    last_run_at: models.DateTimeField[datetime | None, datetime | None] = models.DateTimeField(
        null=True, blank=True
    )
    last_status: models.CharField[str | None, str | None] = models.CharField(
        max_length=20,
        choices=Status.choices,
        null=True,
        blank=True,
    )
    last_raw_text: models.TextField[str | None, str | None] = models.TextField(
        null=True, blank=True
    )
    last_processed_text: models.TextField[str | None, str | None] = models.TextField(
        null=True, blank=True
    )
    last_error_message: models.TextField[str | None, str | None] = models.TextField(
        null=True, blank=True
    )
    last_duration_ms: models.IntegerField[int | None, int | None] = models.IntegerField(
        null=True, blank=True
    )

    active: models.BooleanField[bool, bool] = models.BooleanField(default=True)

    created_at: models.DateTimeField[datetime, datetime] = models.DateTimeField(auto_now_add=True)
    updated_at: models.DateTimeField[datetime, datetime] = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["name"]

    def __str__(self) -> str:
        """Return the target's display name."""
        return self.name


class Run(models.Model):
    """One execution sweep over all active targets."""

    class Status(models.TextChoices):
        SUCCESS = "success", "Success"
        PARTIAL = "partial", "Partial"
        FAILURE = "failure", "Failure"

    started_at: models.DateTimeField[datetime, datetime] = models.DateTimeField(auto_now_add=True)
    finished_at: models.DateTimeField[datetime | None, datetime | None] = models.DateTimeField(
        null=True, blank=True
    )

    status: models.CharField[str, str] = models.CharField(max_length=20, choices=Status.choices)
    error_summary: models.TextField[str | None, str | None] = models.TextField(
        null=True, blank=True
    )

    class Meta:
        ordering = ["-id"]

    def __str__(self) -> str:
        """Return a short description of the run."""
        return f"Run {self.pk} ({self.status})"


class Observation(models.Model):
    """The result of checking a single target within a run."""

    run: models.ForeignKey[Run, Run] = models.ForeignKey(
        Run, on_delete=models.CASCADE, related_name="observations"
    )
    run_id: int
    target: models.ForeignKey[Target, Target] = models.ForeignKey(
        Target, on_delete=models.CASCADE, related_name="observations"
    )
    target_id: int

    observed_at: models.DateTimeField[datetime, datetime] = models.DateTimeField(auto_now_add=True)

    raw_text: models.TextField[str | None, str | None] = models.TextField(null=True, blank=True)
    processed_text: models.TextField[str | None, str | None] = models.TextField(
        null=True, blank=True
    )

    changed: models.BooleanField[bool, bool] = models.BooleanField(default=False)
    previous_processed_text: models.TextField[str | None, str | None] = models.TextField(
        null=True, blank=True
    )

    error_message: models.TextField[str | None, str | None] = models.TextField(
        null=True, blank=True
    )
    duration_ms: models.IntegerField[int | None, int | None] = models.IntegerField(
        null=True, blank=True
    )

    class Meta:
        ordering = ["-id"]

    def __str__(self) -> str:
        """Return a short description of the observation."""
        return f"Observation {self.pk} (target={self.target_id}, run={self.run_id})"
