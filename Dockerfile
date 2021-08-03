FROM python:3.7-buster

LABEL maintainer='analytics@valuestreambiz.com'

ENV PYTHONUNBUFFERED 1

COPY ./requirements.txt /requirements.txt
COPY ./app /app
COPY ./scripts /scripts

EXPOSE 8000
WORKDIR /app

RUN python -m venv /py && \
    /py/bin/pip install --upgrade pip && \
    /py/bin/pip install -r /requirements.txt && \
    # adduser --disabled-password --no-create-home msi_user && \
    mkdir -p /vol/web/assets &&  \
    mkdir -p /vol/web/media && \
    # chown -R msi_user:msi_user /vol && \
    # chmod -R 755 /vol && \
    chmod -R +x /scripts && \
    echo "deb http://ftp.hk.debian.org/debian buster main" | tee -a /etc/apt/sources.list && \
    apt-get update && apt-get -y install cron

# RUN chgrp msi_user /var/run/crond.pid && \
#     usermod -a -G msi_user msi_user

RUN chmod a+x /app/django_app/schedule_script.py /app/django_app/global_functions.py && \
    chmod -R 777 /app/django_app/media

ENV PATH="/scripts:/py/bin:$PATH"

USER root

CMD [ "run.sh" ]