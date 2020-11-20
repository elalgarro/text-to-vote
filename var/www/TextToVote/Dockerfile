FROM tiangolo/uwsgi-nginx-flask:python3.6-alpine3.7

RUN apk add --no-cache --update  bash nano

RUN set -e; \
        apk add --no-cache --virtual .build-deps \
            gcc \
            libc-dev \
            linux-headers \
            mariadb-dev \
            postgresql-dev

ENV STATIC_URL /static
ENV STATIC_PATH /var/www/app/static

ARG app_path=/var/www/
COPY ./requirements.txt /var/www/requirements.txt
RUN pip3 --no-cache install -r /var/www/requirements.txt
