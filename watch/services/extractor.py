"""HTML text extraction via CSS and XPath selectors."""

from __future__ import annotations

from typing import Any, cast

from lxml import html

from watch.models import Target


def extract_texts(html_text: str, selector_type: str, selector: str) -> list[str]:
    """Extract node texts from HTML using XPath or CSS selectors."""
    doc = html.fromstring(html_text)
    nodes: list[Any] = []

    if selector_type == Target.SelectorType.CSS.value:
        nodes = doc.cssselect(selector)
    elif selector_type == Target.SelectorType.XPATH.value:
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

    return [stripped for t in texts if (stripped := t.strip())]


def _node_text(node: Any) -> str:
    """Extract string content from a parsed lxml node."""
    if isinstance(node, str):
        return node

    if hasattr(node, "text_content") and callable(node.text_content):
        return str(node.text_content())

    return str(node)
