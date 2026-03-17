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
trap 'docker compose down' EXIT

echo "Syncing dependencies..."
uv sync

echo "Running migrations..."
.venv/bin/alembic upgrade head

echo "Starting Flask dev server..."
.venv/bin/flask --app 'app:create_app()' run --host=0.0.0.0 --port=${FLASK_PORT:-8000}
