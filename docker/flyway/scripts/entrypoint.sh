#!/bin/bash
set -e
sleep 1

echo "🚀 Инициализация пользователя..."
../scripts/init-migrator.sh

echo "👤 Создание роли аналитика..."
../scripts/create_analytics_role.sh

echo "✅ Настройка базы данных завершена."
