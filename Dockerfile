FROM python:3.6-alpine3.7
CMD python manage.py runserver 0.0.0.0:8000
EXPOSE 8000
ENV PYTHONUNBUFFERED=1

COPY requirements.txt /opt/vraagdepolitiek/requirements.txt

RUN apk add --no-cache --virtual .build-deps \
    build-base \
    py-mysqldb \
    gcc \
    libc-dev \
    libffi-dev \
    mariadb-dev \
    && apk add \
    mariadb-client-libs \
    jpeg-dev \
    && pip install -r /opt/vraagdepolitiek/requirements.txt \
    && apk del .build-deps

WORKDIR /opt/vraagdepolitiek
COPY . /opt/vraagdepolitiek
COPY vraagdepolitiek/local_settings.docker.py vraagdepolitiek/local_settings.py

COPY --from=vraagdepolitiek_frontend /opt/vraagdepolitiek/frontend/out /opt/vraagdepolitiek/frontend/out
RUN python manage.py collectstatic --noinput
