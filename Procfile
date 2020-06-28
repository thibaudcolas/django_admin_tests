web: gunicorn django_admin_tests.wsgi
release: ./manage.py migrate && ./manage.py loaddata fixtures.json
