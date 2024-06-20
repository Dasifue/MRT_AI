#!/bin/sh

until cd /app/backend

until python3 manage.py migrate

python3 manage.py collectstatic --noinput

# python manage.py createsuperuser --noinput

exec gunicorn main.wsgi:application --bind 0.0.0.0:8000 --workers 4 --threads 4