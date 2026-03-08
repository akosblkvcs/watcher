# Base stage
FROM python:3.12-slim as base

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

RUN apt-get update \
  && apt-get install -y --no-install-recommends ca-certificates \
  && rm -rf /var/lib/apt/lists/*

# Development stage
FROM base as development

COPY pyproject.toml README.md ./
COPY src ./src
COPY alembic ./alembic
COPY alembic.ini dev-start.sh ./

RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -e .[development] \
    && chmod +x /dev-start.sh

EXPOSE 8000

CMD ["sh", "dev-start.sh"]

# Production stage
FROM base AS production

COPY pyproject.toml README.md ./
COPY src ./src
COPY alembic ./alembic
COPY alembic.ini ./

RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir .

RUN addgroup --system appgroup \
    && adduser --system --group appuser \
    && chown -R appuser:appgroup /app

USER appuser

EXPOSE 8000

CMD ["gunicorn", "-w", "2", "-b", "0.0.0.0:8000", "web.app:create_app()"]
