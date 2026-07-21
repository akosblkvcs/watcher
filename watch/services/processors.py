import re
from collections.abc import Callable
from typing import Any

from watch.models import Target

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
        clean_v = re.sub(r"\s+", "", v)

        if is_comma:
            # Assumes dot is the thousands separator: 1.234,56 -> 1234.56
            text = clean_v.replace(".", "").replace(",", ".")
        else:
            # Assumes comma is the thousands separator: 1,234.56 -> 1234.56
            text = clean_v.replace(",", "")

        if match := re.search(r"\d+(?:\.\d+)?", text):
            nums.append(float(match.group(0)))

    if not nums:
        return empty

    return f"{min(nums):g}"


PROCESSORS: dict[str, Processor] = {
    Target.ProcessorType.RAW_TEXT: raw_text,
    Target.ProcessorType.MIN_VALUE: min_value,
}
