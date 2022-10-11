FROM postgres:latest

ENV POSTGRES_PASSWORD=secret

ENV POSTGRES_USER=username

ENV POSTGRES_DB=database

COPY numbers_api.sql /docker-entrypoint-initdb.d/numbers_api.sql