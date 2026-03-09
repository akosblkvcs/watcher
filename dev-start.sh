#!/bin/sh
set -e

echo "Running migrations..."
.venv/bin/alembic upgrade head

echo "Starting Flask dev server..."
exec .venv/bin/flask --app 'web.app:create_app()' run --host=0.0.0.0 --port=8000
