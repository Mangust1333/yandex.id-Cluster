#!/bin/bash

set -e

echo "--- CHECKING IF MIGRATOR ROLE EXISTS ---"

ROLE_EXISTS=$(PGPASSWORD="$POSTGRES_PASSWORD" psql -h "$POSTGRES_HOST" -U "$POSTGRES_USER" -d postgres -t -c "
  SELECT 1 FROM pg_roles WHERE rolname='analytic';
")

if [ -z "$ROLE_EXISTS" ]; then
  echo "--- CREATING ANALYTIC ROLE ---"
  PGPASSWORD="$POSTGRES_PASSWORD" psql -h "$POSTGRES_HOST" -U "$POSTGRES_USER" -d postgres -c "
    CREATE ROLE analytic NOLOGIN INHERIT;
  "
else
  echo "--- GROUP ROLE 'analytic' ALREADY EXISTS ---"
fi

echo "--- GRANTING PRIVILEGES TO 'analytic' ROLE ---"
PGPASSWORD="$POSTGRES_PASSWORD" psql -h "$POSTGRES_HOST" -U "$POSTGRES_USER" -d postgres -c "
  GRANT USAGE ON SCHEMA public TO analytic;
  GRANT SELECT ON ALL TABLES IN SCHEMA public TO analytic;
  ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT SELECT ON TABLES TO analytic;
"

IFS=',' read -ra USERS <<< "$ANALYST_NAMES"

for USERNAME in "${USERS[@]}"; do
  USERNAME=$(echo "$USERNAME" | xargs)
  echo "--- CREATING USER: $USERNAME ---"
  PGPASSWORD="$POSTGRES_PASSWORD" psql -h "$POSTGRES_HOST" -U "$POSTGRES_USER" -d postgres -c "
    DO \$\$
    BEGIN
      IF NOT EXISTS (SELECT FROM pg_catalog.pg_roles WHERE rolname = '${USERNAME}') THEN
        CREATE ROLE ${USERNAME} WITH LOGIN PASSWORD '${USERNAME}_123' INHERIT;
      END IF;
      GRANT analytic TO ${USERNAME};
    END
    \$\$;
  "
done
