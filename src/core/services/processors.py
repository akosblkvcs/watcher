"""
Value processors for extracted text.
"""

from __future__ import annotations

import re
from collections.abc import Callable
from typing import Any


Processor = Callable[[list[str], dict[str, Any]], str]
"""Processor signature: (values, config) -> processed string."""


def raw_text(values: list[str], _: dict[str, Any]) -> str:
    """Clean values and join them into a single comma-separated string."""
    cleaned = [v.strip() for v in values if v and v.strip()]
    return ", ".join(cleaned)


def min_value(values: list[str], config: dict[str, Any]) -> str:
    """
    Parse numbers from values and return the minimum (or empty_value if none).
    """
    empty_value = str(config.get("empty_value", "-"))
    decimal_sep = str(config.get("decimal_sep", "."))

    nums: list[float] = []
    for v in values:
        if not v:
            continue

        t = re.sub(r"[^\d,\.]", "", v.strip())
        if not t:
            continue

        if decimal_sep == ",":
            t = t.replace(".", "")
            t = t.replace(",", ".")
        else:
            t = t.replace(",", "")

        m = re.search(r"\d+(\.\d+)?", t)
        if not m:
            continue

        try:
            nums.append(float(m.group(0)))
        except ValueError:
            continue

    return empty_value if not nums else str(min(nums))


PROCESSORS: dict[str, Processor] = {
    "raw_text": raw_text,
    "min_value": min_value,
}
