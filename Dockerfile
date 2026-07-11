# Base stage
FROM python:3.14-slim AS base

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    UV_LINK_MODE=copy

COPY --from=ghcr.io/astral-sh/uv:0.10.9 /uv /uvx /bin/

# Builder stage for production
FROM base AS builder

COPY pyproject.toml uv.lock ./

RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --locked --no-dev --compile-bytecode --group prod

COPY manage.py ./
COPY config ./config
COPY watch ./watch
COPY templates ./templates
COPY static ./static

RUN DJANGO_SETTINGS_MODULE=config.settings_build \
    /app/.venv/bin/python manage.py collectstatic --noinput

# Production stage
FROM python:3.14-slim AS production

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PATH="/app/.venv/bin:$PATH" \
    DJANGO_SETTINGS_MODULE=config.settings

RUN apt-get update \
    && apt-get install -y --no-install-recommends wget \
    && rm -rf /var/lib/apt/lists/*

RUN addgroup --system appgroup \
    && adduser --system --ingroup appgroup appuser

COPY --from=builder --chown=appuser:appgroup /app/.venv /app/.venv
COPY --from=builder --chown=appuser:appgroup /app/manage.py /app/manage.py
COPY --from=builder --chown=appuser:appgroup /app/config /app/config
COPY --from=builder --chown=appuser:appgroup /app/watch /app/watch
COPY --from=builder --chown=appuser:appgroup /app/templates /app/templates
COPY --from=builder --chown=appuser:appgroup /app/staticfiles /app/staticfiles

USER appuser

EXPOSE 8000

STOPSIGNAL SIGTERM

CMD ["sh", "-c", "\
     python manage.py migrate --noinput && \
     exec gunicorn \
         --preload \
         -w 2 \
         -b 0.0.0.0:8000 \
         --access-logfile - \
         --error-logfile - \
         --max-requests 1000 \
         --max-requests-jitter 100 \
         config.wsgi:application \
"]
