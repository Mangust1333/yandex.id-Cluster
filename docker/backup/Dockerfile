FROM alpine:latest

RUN apk add --no-cache postgresql-client bash curl

COPY backup.sh /backup.sh
COPY cronjob /etc/crontabs/root
COPY entrypoint.sh /entrypoint.sh

RUN chmod +x /backup.sh /entrypoint.sh

CMD ["/entrypoint.sh"]
