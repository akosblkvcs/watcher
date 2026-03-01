from __future__ import annotations

from dataclasses import dataclass

from core.services.extractor import extract_texts_from_html
from core.services.fetcher import fetch_html
from core.services.processors import PROCESSORS


@dataclass(frozen=True)
class PipelineParams:
    """Pipeline input parameters."""

    url: str
    selector_type: str
    selector: str
    processor_type: str
    processor_config: dict[str, object] | None


@dataclass(frozen=True)
class PipelineResult:
    """Pipeline output containing raw and processed text."""

    raw_text: str
    processed_text: str


def run_pipeline(*, params: PipelineParams) -> PipelineResult:
    """Run fetch -> extract -> process pipeline and return raw and processed text."""
    fetch = fetch_html(params.url)

    extracted = extract_texts_from_html(
        fetch.text,
        selector_type=params.selector_type,
        selector=params.selector,
    )
    raw = ", ".join(extracted.texts)

    processor = PROCESSORS.get(params.processor_type)

    if processor is None:
        raise ValueError(f"Unknown processor_type: {params.processor_type}")

    processed = processor(extracted.texts, params.processor_config or {})

    return PipelineResult(raw_text=raw, processed_text=processed)
