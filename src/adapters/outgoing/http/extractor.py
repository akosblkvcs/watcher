from __future__ import annotations

from dataclasses import dataclass
from typing import Any, cast

from lxml import html


@dataclass(frozen=True)
class ExtractResult:
    """Container for extracted texts."""

    texts: list[str]


def extract_texts_from_html(
    html_text: str,
    selector_type: str,
    selector: str,
) -> ExtractResult:
    """Extract node texts from HTML using XPath or CSS selectors."""
    doc = html.fromstring(html_text)
    nodes: list[Any] = []

    if selector_type == "css":
        nodes = doc.cssselect(selector)
    elif selector_type == "xpath":
        nodes_obj = doc.xpath(selector)
        if isinstance(nodes_obj, list):
            nodes = cast(list[Any], nodes_obj)
        elif isinstance(nodes_obj, tuple):
            nodes = list(cast(tuple[Any, ...], nodes_obj))
        else:
            nodes = [nodes_obj]
    else:
        raise ValueError(f"Unsupported selector_type: {selector_type}")

    texts = [_node_text(n) for n in nodes]

    return ExtractResult(texts=_clean(texts))


def _node_text(node: Any) -> str:
    """Extract string content from a parsed lxml node."""
    if isinstance(node, str):
        return node

    if hasattr(node, "text_content") and callable(node.text_content):
        return str(node.text_content())

    return str(node)


def _clean(values: list[str]) -> list[str]:
    """Remove empty elements and strip whitespace from strings."""
    return [stripped for v in values if (stripped := v.strip())]
