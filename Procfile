web: /opt/venv/bin/python manage.py migrate --noinput && /opt/venv/bin/gunicorn allin_django.wsgi --bind 0.0.0.0:$PORT --workers 2 --timeout 120 --log-file -
