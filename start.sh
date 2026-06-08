#!/bin/bash
set -e
echo '=== Migrations ==='
python manage.py migrate --noinput
echo '=== Collectstatic ==='
python manage.py collectstatic --noinput
echo '=== Gunicorn ==='
exec gunicorn allin_django.wsgi --bind "0.0.0.0:${PORT:-8000}" --workers 2 --timeout 120 --access-logfile - --error-logfile -
