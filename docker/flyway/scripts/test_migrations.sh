#!/bin/bash

set -e

MIGRATIONS_DIR="/flyway/migrations"
SNAPSHOT_DIR="./snapshots"
mkdir -p "$SNAPSHOT_DIR"


MIGRATION_FILES=($(ls "$MIGRATIONS_DIR" | grep -E '^[V][0-9]+__.*\.sql$' | sort))

dump_schema() {
  echo "=============================="
  echo "Сохранение $suffix состояния схемы версии $version"
  echo "=============================="
  local version=$1
  local suffix=$2

  PGPASSWORD="${POSTGRES_PASSWORD}" pg_dump --schema-only --no-owner \
    --file="${SNAPSHOT_DIR}/schema_${version}_${suffix}.sql" \
    -h "${POSTGRES_HOST}" -p "${POSTGRES_PORT}" \
    -U "${POSTGRES_USER}" -d "${POSTGRES_DB}"
}

migrate_to() {
  local version=$1
  echo "=============================="
  echo "Применение миграции до версии $version"
  echo "=============================="
  flyway migrate -locations="filesystem:$MIGRATIONS_DIR" -target="$version"
}

undo_migration() {
  local version=$1
  
  echo "=============================="
  echo "Откат миграции $version"
  echo "=============================="
  MIGRATION_VERSION="$version" \
  POSTGRES_HOST="$POSTGRES_HOST" \
  POSTGRES_PORT="$POSTGRES_PORT" \
  POSTGRES_USER="$POSTGRES_USER" \
  TARGET_DB="$POSTGRES_DB" \
  bash ../scripts/undo.sh
}

for file in "${MIGRATION_FILES[@]}"; do
  version=$(echo "$file" | grep -oP '(?<=^V)[0-9]+')

  echo "=============================="
  echo "Проверка миграции версии $version"
  echo "=============================="

  migrate_to "$version"

  dump_schema "$version" "first"

  undo_migration "$((version - 1))"

  migrate_to "$version"

  dump_schema "$version" "second"

  echo "=============================="
  echo "Сравнение дампов для версии $version..."
  echo "=============================="
  if diff -q "${SNAPSHOT_DIR}/schema_${version}_first.sql" "${SNAPSHOT_DIR}/schema_${version}_second.sql"; then
    echo "Миграция $version идемпотентна"
  else
    echo "Миграция $version НЕ идемпотентна"
    exit 1
  fi
done

echo "=============================="
echo "Все миграции успешно прошли проверку на идемпотентность!"
echo "=============================="