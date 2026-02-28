"""
HTML text extraction helpers using lxml.
"""

# pyright: reportUnknownMemberType=false

from __future__ import annotations

from dataclasses import dataclass

from lxml import html


@dataclass(frozen=True)
class ExtractResult:
    """Extraction output container."""
    texts: list[str]


def extract_texts_from_html(
    html_text: str,
    selector_type: str,
    selector: str,
) -> ExtractResult:
    """
    Extract node texts from HTML using the given selector type and selector.
    """
    doc = html.fromstring(html_text)

    if selector_type == "css":
        raise ValueError("The css selector_type is not wired yet.")

    if selector_type == "xpath":
        nodes_obj: object = doc.xpath(selector)
        if isinstance(nodes_obj, (list, tuple)):
            nodes: list[object] = list(nodes_obj)
        else:
            nodes = [nodes_obj]
        texts = [_node_text(n) for n in nodes]
        return ExtractResult(texts=_clean(texts))

    raise ValueError(f"Unsupported selector_type: {selector_type}")


def _node_text(node: object) -> str:
    """Return textual content for an lxml node or a raw string result."""
    if isinstance(node, str):
        return node

    if hasattr(node, "text_content"):
        text_content = getattr(node, "text_content")
        if callable(text_content):
            return str(text_content())

    return str(node)


def _clean(values: list[str]) -> list[str]:
    """Strip, drop empties, and normalize extracted strings."""
    return [v.strip() for v in values if v.strip()]
