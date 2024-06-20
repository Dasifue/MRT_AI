#!/bin/sh

until cd /app/backend

# run a worker :)
exec celery -A main worker --loglevel=info --concurrency 1 -E
