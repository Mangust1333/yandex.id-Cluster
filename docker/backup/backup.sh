#!/bin/bash

set -e

TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
BACKUP_FILE="/backups/backup_${TARGET_DB}_${TIMESTAMP}.sql"

echo "🗄️ Создание бэкапа: $BACKUP_FILE"
PGPASSWORD="${POSTGRES_PASSWORD}" pg_dump -h "${POSTGRES_HOST}" -p "${POSTGRES_PORT}" -U "${POSTGRES_USER}" -F c -d "${TARGET_DB}" -f "${BACKUP_FILE}"


BACKUPS=($(ls -1t /backups/backup_${TARGET_DB}_*.sql))
COUNT=${#BACKUPS[@]}

if [ "$COUNT" -gt "$BACKUP_RETENTION_COUNT" ]; then
    echo "Удаление старых бэкапов (оставляем $BACKUP_RETENTION_COUNT)"
    for ((i=BACKUP_RETENTION_COUNT;i<COUNT;i++)); do
        echo "Удаляем: ${BACKUPS[$i]}"
        rm -f "${BACKUPS[$i]}"
    done
fi
