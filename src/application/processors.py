"""Text processors that transform extracted content."""

from __future__ import annotations

import re
from collections.abc import Callable
from typing import Any

from domain.enums import ProcessorType

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
        # 1. Remove all whitespace
        clean_v = re.sub(r"\s+", "", v)

        # 2. Normalize based on separator config
        if is_comma:
            # Assumes dot is thousands separator: 1.234,56 -> 1234.56
            text = clean_v.replace(".", "").replace(",", ".")
        else:
            # Assumes comma is thousands separator: 1,234.56 -> 1234.56
            text = clean_v.replace(",", "")

        # 3. Extract the numeric component
        if match := re.search(r"\d+(?:\.\d+)?", text):
            nums.append(float(match.group(0)))

    if not nums:
        return empty

    return f"{min(nums):g}"


PROCESSORS: dict[ProcessorType, Processor] = {
    ProcessorType.RAW_TEXT: raw_text,
    ProcessorType.MIN_VALUE: min_value,
}
