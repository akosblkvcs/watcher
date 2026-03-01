# Base stage
FROM python:3.12-slim as base

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

RUN apt-get update \
  && apt-get install -y --no-install-recommends ca-certificates \
  && rm -rf /var/lib/apt/lists/*

COPY pyproject.toml README.md ./

# Development stage
FROM base as development

COPY src /app/src

RUN pip install --no-cache-dir -U pip && pip install --no-cache-dir -e .

CMD ["flask", "run", "--host=0.0.0.0", "--reload"]

# Production stage
FROM base as production

COPY src /app/src
COPY alembic /app/alembic
COPY alembic.ini /app/

RUN pip install --no-cache-dir -U pip && pip install --no-cache-dir .

EXPOSE 8000

CMD ["gunicorn", "-w", "2", "-b", "0.0.0.0:8000", "web.app:create_app()"]
