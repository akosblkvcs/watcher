# Base stage
FROM python:3.12-slim AS base

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    UV_LINK_MODE=copy

WORKDIR /app

COPY --from=ghcr.io/astral-sh/uv:0.10.9 /uv /uvx /bin/

# Development stage
FROM base AS development

COPY pyproject.toml uv.lock README.md ./

RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --locked --no-install-project

COPY src ./src
COPY alembic ./alembic
COPY alembic.ini dev-start.sh ./

RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --locked \
    && chmod +x /app/dev-start.sh

EXPOSE 8000

CMD sh dev-start.sh

# Builder stage for production
FROM base AS builder

COPY pyproject.toml uv.lock README.md ./

RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --locked --no-dev --no-editable --no-install-project --group prod

COPY src ./src
COPY alembic ./alembic
COPY alembic.ini ./

RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --locked --no-dev --no-editable --compile-bytecode --group prod

# Production stage
FROM python:3.12-slim AS production

ENV PYTHONUNBUFFERED=1 \
    PATH="/app/.venv/bin:$PATH"

WORKDIR /app

RUN rm -rf /var/lib/apt/lists/* \
    && addgroup --system appgroup \
    && adduser --system --ingroup appgroup appuser

COPY --from=builder --chown=appuser:appgroup /app/.venv /app/.venv
COPY --from=builder --chown=appuser:appgroup /app/src /app/src
COPY --from=builder --chown=appuser:appgroup /app/alembic /app/alembic
COPY --from=builder --chown=appuser:appgroup /app/alembic.ini /app/alembic.ini

USER appuser

EXPOSE 8000

CMD exec gunicorn \
    -w "${WEB_CONCURRENCY:-2}" \
    -b 0.0.0.0:8000 \
    --access-logfile - \
    "app:create_app()"
