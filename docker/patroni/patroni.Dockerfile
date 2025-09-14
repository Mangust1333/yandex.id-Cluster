FROM ongres/patroni:latest

USER root

RUN mkdir -p /data/patroni \
    && chown postgres:postgres /data/patroni \
    && chmod 700 /data/patroni

USER postgres

COPY patroni.yml /etc/patroni.yml
ENTRYPOINT ["patroni", "/etc/patroni.yml"]
