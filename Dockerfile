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
    adduser --disabled-password --no-create-home msi_user && \
    mkdir -p /vol/web/assets &&  \
    mkdir -p /vol/web/media && \
    chown -R msi_user:msi_user /vol && \
    chmod -R 755 /vol && \
    chmod -R +x /scripts

ENV PATH="/scripts:/py/bin:$PATH"

USER msi_user

CMD [ "run.sh" ]