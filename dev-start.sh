#!/bin/sh
set -e

alembic upgrade head
exec flask --app 'web.app:create_app()' run --host=0.0.0.0 --port=8000 --reload
