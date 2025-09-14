FROM flyway/flyway:10

RUN apt-get update && apt-get install -y postgresql-client && rm -rf /var/lib/apt/lists/*
