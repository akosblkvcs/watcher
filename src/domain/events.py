"""Domain events via blinker signals.

Provides a lightweight pub/sub mechanism for decoupled communication
between application components. Subscribers can connect to any signal
to react to domain-level occurrences without tight coupling.

Example usage::

    from domain.events import target_changed

    @target_changed.connect
    def on_change(sender, **kwargs):
        observation = kwargs["observation"]
        ...
"""

from __future__ import annotations

from blinker import Namespace

_ns = Namespace()

target_checked = _ns.signal("target-checked")
"""Fired after each target is processed (success or failure)."""

target_changed = _ns.signal("target-changed")
"""Fired when a target's processed text differs from its previous value."""

run_started = _ns.signal("run-started")
"""Fired when a new watcher run begins."""

run_completed = _ns.signal("run-completed")
"""Fired when a watcher run finishes (success or partial)."""
