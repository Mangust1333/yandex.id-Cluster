#!/bin/bash

set -e

echo "--- CHECKING IF MIGRATOR ROLE EXISTS ---"

ROLE_EXISTS=$(PGPASSWORD="$POSTGRES_PASSWORD" psql -h "$POSTGRES_HOST" -U "$POSTGRES_USER" -d postgres -t -c "
  SELECT 1 FROM pg_roles WHERE rolname='migrator';
")

if [ -z "$ROLE_EXISTS" ]; then
  echo "--- CREATING MIGRATOR ROLE ---"
  
  PGPASSWORD="$POSTGRES_PASSWORD" psql -h "$POSTGRES_HOST" -U "$POSTGRES_USER" -d postgres -c "
    CREATE ROLE migrator WITH LOGIN PASSWORD '$MIGRATOR_PASSWORD';
    ALTER ROLE migrator WITH CREATEDB;
    GRANT USAGE, CREATE ON SCHEMA public TO migrator;
  "
else
  echo "--- MIGRATOR ROLE ALREADY EXISTS ---"
fi
