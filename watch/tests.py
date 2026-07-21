from django.test import TestCase
from django.urls import reverse

from watch.models import Run, Target
from watch.services.processors import min_value, raw_text
from watch.services.runner import is_changed, run_all


class ProcessorTests(TestCase):
    """Unit tests for text processors."""

    def test_raw_text_joins_and_strips(self) -> None:
        """Values are stripped and joined with commas; empties dropped."""
        self.assertEqual(raw_text(["  a ", "", "b"], {}), "a, b")

    def test_min_value_dot_decimal(self) -> None:
        """Comma is treated as thousands separator by default."""
        self.assertEqual(min_value(["1,234.56 USD", "999.99 USD"], {}), "999.99")

    def test_min_value_comma_decimal(self) -> None:
        """With decimal_sep=',' the dot is the thousands separator."""
        self.assertEqual(min_value(["1.234,56", "999,99"], {"decimal_sep": ","}), "999.99")

    def test_min_value_empty(self) -> None:
        """Returns the configured placeholder when nothing parses."""
        self.assertEqual(min_value(["no numbers"], {"empty_value": "-"}), "-")


class DiffTests(TestCase):
    """Unit tests for change detection."""

    def test_both_none_is_unchanged(self) -> None:
        """Two missing values are not a change."""
        self.assertFalse(is_changed(None, None))

    def test_none_to_value_is_changed(self) -> None:
        """Appearing or disappearing values are a change."""
        self.assertTrue(is_changed(None, "x"))

    def test_whitespace_normalized(self) -> None:
        """Surrounding whitespace does not count as a change."""
        self.assertFalse(is_changed(" x ", "x"))


class RunnerStatusTests(TestCase):
    """Integration tests for run status computation."""

    def test_all_targets_failing_marks_run_failed(self) -> None:
        """A run where every target fails is FAILURE, not PARTIAL."""
        # Port 1 is never listening; the fetch fails with connection refused.
        Target.objects.create(name="Down", url="http://127.0.0.1:1/", selector="h1")

        result = run_all()

        run = Run.objects.get(pk=result.run_id)
        self.assertEqual(run.status, Run.Status.FAILURE)
        self.assertEqual(result.targets_failed, 1)
        self.assertIsNotNone(run.finished_at)

    def test_no_targets_is_success(self) -> None:
        """An empty run has nothing failing, so it counts as SUCCESS."""
        result = run_all()

        run = Run.objects.get(pk=result.run_id)
        self.assertEqual(run.status, Run.Status.SUCCESS)
        self.assertEqual(result.targets_total, 0)


class TargetViewTests(TestCase):
    """Integration tests for target views."""

    def test_create_route_is_disabled(self) -> None:
        """The self-serve create endpoint is retired; targets come from the admin."""
        resp = self.client.post("/targets/new/", {"name": "Example"})

        self.assertEqual(resp.status_code, 404)
        self.assertFalse(Target.objects.exists())

    def test_create_page_is_not_linked_from_list(self) -> None:
        """The list page must not link to the retired create endpoint."""
        resp = self.client.get(reverse("watch:target-list"))

        self.assertNotContains(resp, "/targets/new/")

    def test_list_shows_only_active_targets(self) -> None:
        """Inactive targets are hidden from the list page."""
        Target.objects.create(name="On", url="https://a.example", selector="h1", active=True)
        Target.objects.create(name="Off", url="https://b.example", selector="h1", active=False)

        resp = self.client.get(reverse("watch:target-list"))

        self.assertContains(resp, "On")
        self.assertNotContains(resp, "Off")
