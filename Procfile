web: python manage.py migrate --noinput && gunicorn allin_django.wsgi --bind 0.0.0.0:$PORT --workers 2 --timeout 120 --log-file -
