#!/bin/bash

echo "Waiting for postgres..."

while ! nc -z db 5432; do
    sleep 0.1
done

echo "PostgreSQL started"

rq worker -u redis://redis:6379 &
exec uvicorn app:app --host 0.0.0.0 --port 8000