#!/usr/bin/env bash
set -euo pipefail

docker compose up -d db

echo "Waiting for Postgres..."
until docker compose exec -T db pg_isready -U postgres -d app >/dev/null 2>&1; do
  sleep 1
done

export $(cat .env | xargs)

python -m alembic upgrade head
pytest -q
