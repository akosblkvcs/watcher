#!/bin/sh
set -e

if [ ! -f .env ]; then
  echo "Error: .env file not found. Copy .env.example and configure it." >&2
  exit 1
fi

set -a
. ./.env
set +a

echo "Starting infrastructure..."
docker compose up -d

echo "Waiting for PostgreSQL..."
until docker compose exec -T postgres pg_isready -U postgres -d watcher -q 2>/dev/null; do
  sleep 1
done

echo "Syncing dependencies..."
uv sync --locked

echo "Running migrations..."
.venv/bin/alembic upgrade head

echo "Starting Flask dev server..."
exec .venv/bin/flask --app 'app:create_app()' run --host=127.0.0.1 --port="${FLASK_PORT:-8000}"
