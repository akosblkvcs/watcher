"""
Change detection helpers for comparing stored vs current text values.
"""

from __future__ import annotations


def is_changed(previous: str | None, current: str | None) -> bool:
    """
    Return True if the normalized values differ, treating None as missing.
    """
    if previous is None and current is None:
        return False
    if previous is None or current is None:
        return True
    return previous.strip() != current.strip()
