from __future__ import annotations

import re
from collections.abc import Callable
from typing import Any

Processor = Callable[[list[str], dict[str, Any]], str]
"""Processor signature: (values, config) -> processed string."""


def raw_text(values: list[str], _config: dict[str, Any]) -> str:
    """Clean values and join them into a single comma-separated string."""
    return ", ".join([stripped for v in values if (stripped := v.strip())])


def min_value(values: list[str], config: dict[str, Any]) -> str:
    """Parse numbers from values and return the minimum."""
    empty = str(config.get("empty_value", "-"))
    is_comma = str(config.get("decimal_sep", ".")) == ","

    nums: list[float] = []
    for v in values:
        text = v.replace(".", "").replace(",", ".") if is_comma else v.replace(",", "")

        if match := re.search(r"\d+(?:\.\d+)?", text):
            nums.append(float(match.group(0)))

    return str(min(nums)) if nums else empty


PROCESSORS: dict[str, Processor] = {
    "raw_text": raw_text,
    "min_value": min_value,
}
