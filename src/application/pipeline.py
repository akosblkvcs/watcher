"""Fetch -> extract -> process orchestration pipeline."""

from __future__ import annotations

from dataclasses import dataclass

from application.ports import Extractor, Fetcher
from application.processors import PROCESSORS
from domain.enums import ProcessorType, SelectorType


@dataclass(frozen=True)
class PipelineParams:
    """Pipeline input parameters."""

    url: str
    selector_type: SelectorType
    selector: str
    processor_type: ProcessorType
    processor_config: dict[str, object] | None


@dataclass(frozen=True)
class PipelineResult:
    """Pipeline output containing raw and processed text."""

    raw_text: str
    processed_text: str


class Pipeline:
    """Orchestrates fetch -> extract -> process using injected adapters."""

    def __init__(self, fetcher: Fetcher, extractor: Extractor) -> None:
        """Create with outbound port implementations."""
        self._fetcher = fetcher
        self._extractor = extractor

    def execute(self, params: PipelineParams) -> PipelineResult:
        """Run the full pipeline and return raw and processed text."""
        fetch = self._fetcher(params.url)

        extracted = self._extractor(
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
