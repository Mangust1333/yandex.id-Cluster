#!/bin/sh

echo "${BACKUP_INTERVAL_CRON} /backup.sh >> /var/log/cron.log 2>&1" > /etc/crontabs/root
crond -f -l 2
