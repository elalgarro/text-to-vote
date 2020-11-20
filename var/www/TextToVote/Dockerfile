FROM tiangolo/uwsgi-nginx-flask:python3.6-alpine3.7

RUN apk add --no-cache --update  bash nano
# RUN apk add --no-cache python3-dev \
#     && apk add py3-pip \
#     && pip3 install --upgrade pip

RUN set -e; \
        apk add --no-cache --virtual .build-deps \
            gcc \
            libc-dev \
            linux-headers \
            mariadb-dev \
            postgresql-dev

# RUN apk add --no-cache --update \
#       py3-gevent \
#       uwsgi \
#       uwsgi-python3 \
#       uwsgi-http \
#       uwsgi-gevent3

# RUN apk add --no-cache --update \
#     openrc \
#     apache2


ENV STATIC_URL /static
ENV STATIC_PATH /var/www/app/static

ARG app_path=/var/www/
# WORKDIR $app_path
#RUN  rc-service apache2 restart
# COPY ./000-default.conf /etc/apache2/sites-available/
# COPY ./app $app_path/
# WORKDIR $app_path/
# COPY ./app.wsgi .
COPY ./requirements.txt /var/www/requirements.txt
RUN pip3 --no-cache install -r /var/www/requirements.txt

# EXPOSE 80
# CMD ["httpd", "-D", "FOREGROUND"]