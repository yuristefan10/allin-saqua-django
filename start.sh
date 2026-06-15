#!/bin/bash
set -e
echo '=== Migrations ==='
python manage.py migrate --noinput
echo '=== Collectstatic ==='
python manage.py collectstatic --noinput
echo '=== Imagens dos pontos ==='
python manage.py baixar_imagens_pontos || true
echo '=== Gunicorn ==='
exec gunicorn allin_django.wsgi --bind "0.0.0.0:${PORT:-8000}" --workers 2 --timeout 120 --access-logfile - --error-logfile -
