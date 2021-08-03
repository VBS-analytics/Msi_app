#!/bin/sh

set -e

ls -la /vol/
ls -la /vol/web

whoami
service cron start
printenv > /etc/default/locale
python manage.py wait_for_db
python manage.py collectstatic --noinput

python manage.py migrate

uwsgi --http :8000 --manage-script-name --module django_project.wsgi --static-map /assets=/vol/web/assets --master --threads 2

# uwsgi --socket :9000 --workers 4 --master --enable-threads --module django_project.wsgi

# uwsgi --http :8000 --workers 4 --master --enable-threads --module django_project.wsgi
# uwsgi --http :8000 --module django_project.wsgi