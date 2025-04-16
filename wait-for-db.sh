#!/bin/sh
set -e

host="$1"
shift
cmd="$@"

until PGPASSWORD="sdfhls**23lasDb2093" psql -h "$host" -U "user1" -d "catalog" -c '\q'; do
  >&2 echo "Postgres is unavailable - sleeping"
  sleep 1
done

>&2 echo "Postgres is up - executing command"
if [ -z "$(ls -A /app/infrastructure/migrations/versions 2>/dev/null)" ]; then
  >&2 echo "No migrations found, creating initial migration"
  alembic revision --autogenerate -m "init"
else
  >&2 echo "Existing migrations detected, skipping autogenerate"
fi
alembic upgrade head
>&2 echo "alembic upgrade head is up - executing command"
exec $cmd