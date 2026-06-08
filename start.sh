#!/bin/bash
set -e

echo "=== Rodando migrations ==="
python manage.py migrate --noinput

echo "=== Coletando arquivos estáticos ==="
python manage.py collectstatic --noinput

echo "=== Iniciando Gunicorn na porta $PORT ==="
exec gunicorn allin_django.wsgi \
    --bind "0.0.0.0:${PORT:-8000}" \
    --workers 2 \
    --timeout 120 \
    --access-logfile - \
    --error-logfile - \
    --log-level info
