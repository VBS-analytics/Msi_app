FROM python:3.7-buster

LABEL maintainer='analytics@valuestreambiz.com'

ENV PYTHONUNBUFFERED 1

COPY ./requirements.txt /requirements.txt
COPY ./app /app
COPY ./scripts /scripts

WORKDIR /app
EXPOSE 8000

RUN python -m venv /py && \
    /py/bin/pip install --upgrade pip && \
    /py/bin/pip install -r /requirements.txt && \
    adduser --disabled-password --no-create-home msi_user && \
    mkdir -p /vol/web/static &&  \
    mkdir -p /vol/web/media && \
    chown -R msi_user /vol && \
    chown -R 755 /vol && \
    chmod -R +x /scripts

ENV PATH="/scripts:/py/bin:$PATH"

USER msi_user

CMD [ "run.sh" ]