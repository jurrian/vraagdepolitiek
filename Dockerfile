FROM python:3.6-alpine3.7

COPY requirements.txt /opt/vragenvuur/requirements.txt

RUN apk add --no-cache --virtual .build-deps \
    build-base \
    py-mysqldb \
    gcc \
    libc-dev \
    libffi-dev \
    mariadb-dev \
    && pip install -r /opt/vragenvuur/requirements.txt \
    && apk add mariadb-client-libs \
    && apk del .build-deps

WORKDIR /opt/vragenvuur
COPY . /opt/vragenvuur
COPY vragenvuur/local_settings.docker.py vragenvuur/local_settings.py

CMD python manage.py runserver 0.0.0.0:8000
EXPOSE 8000
ENV PYTHONUNBUFFERED=1
