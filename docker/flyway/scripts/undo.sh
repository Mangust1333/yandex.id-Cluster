#!/bin/bash

set -e

if [ -z "$MIGRATION_VERSION" ]; then
  echo "MIGRATION_VERSION is not set. Skipping undo."
  exit 0
fi

if ! [[ "$MIGRATION_VERSION" =~ ^[0-9]+$ ]]; then
  echo "ERROR: MIGRATION_VERSION ('$MIGRATION_VERSION') must be a numeric value."
  exit 1
fi

CURRENT_VERSION=$(
  PGPASSWORD="$POSTGRES_PASSWORD" \
  psql -h "$POSTGRES_HOST" -U "$POSTGRES_USER" -d "$TARGET_DB" \
    -tA \
    -c "SELECT version
          FROM flyway_schema_history
         WHERE success = TRUE
      ORDER BY installed_rank DESC
         LIMIT 1;"
)


if ! [[ "$CURRENT_VERSION" =~ ^[0-9]+$ ]]; then
  echo "ERROR: Current migration version ('$CURRENT_VERSION') is not a numeric value."
  exit 1
fi

echo "Current migration version: $CURRENT_VERSION"
echo "Target (MIGRATION_VERSION): $MIGRATION_VERSION"

if [ "$CURRENT_VERSION" -le "$MIGRATION_VERSION" ]; then
  echo "No rollback needed. Current version ($CURRENT_VERSION) <= MIGRATION_VERSION ($MIGRATION_VERSION)"
  exit 0
fi

echo "Starting rollback from $CURRENT_VERSION to $MIGRATION_VERSION"

for (( ver=CURRENT_VERSION; ver>MIGRATION_VERSION; ver-- )); do
  file=$(find /undo -maxdepth 1 -type f -name "U${ver}*.sql" | sort | head -n 1)

  if [ -z "$file" ]; then
    echo "ERROR: Missing undo file for version $ver (expected U${ver}*.sql). Aborting rollback."
    exit 1
  fi

  echo "Running undo script: $file"
  PGPASSWORD="$POSTGRES_PASSWORD" psql -h "$POSTGRES_HOST" -U "$POSTGRES_USER" -d "$TARGET_DB" -f "$file" || { echo "Откат миграции не выполнен"; exit 1; }

  echo "Deleting migration record for version $ver from flyway_schema_history"
  PGPASSWORD="$POSTGRES_PASSWORD" psql -h "$POSTGRES_HOST" -U "$POSTGRES_USER" -d "$TARGET_DB" -c "
    DELETE FROM flyway_schema_history WHERE version = '$ver';
  "
done

echo "--- ROLLBACK DONE ---"
