"""
Provides the main entry point for the watcher worker service.
"""

from __future__ import annotations

from core.config.settings import Settings
from core.services.pipeline import PipelineParams, run_pipeline


def main() -> int:
    """Main entry point for the watcher worker service."""

    settings = Settings()
    settings.validate_required()

    params = PipelineParams(
        url="https://example.com",
        selector_type="xpath",
        selector="//h1",
        processor_type="raw_text",
        processor_config=None,
        user_agent=settings.user_agent,
        timeout_seconds=settings.http_timeout_seconds,
    )

    result = run_pipeline(params=params)

    print(f"raw_text={result.raw_text}")
    print(f"processed_text={result.processed_text}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
