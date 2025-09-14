#!/bin/bash
set -e
sleep 2

echo "📦 Применение миграций с помощью Flyway..."
if [ -z "$MIGRATION_VERSION" ]; then
  flyway migrate
else
  flyway migrate -target=$MIGRATION_VERSION
fi

echo "↩️ Откат миграции, если указана версия..."
if [ -n "$MIGRATION_VERSION" ]; then
  export MIGRATION_VERSION
  ../scripts/undo.sh -MIGRATION_VERSION=$MIGRATION_VERSION
fi

echo "✅ Миграции завершены."