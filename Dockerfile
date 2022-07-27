FROM python:3.9-alpine3.13
LABEL maintainer="wiringconnection.com"

ENV PYTHONBUFERED 1
ENV USER_ID=65536
ENV GROUP_ID=65536
ENV USER_NAME=app
ENV GROUP_NAME=appGroup

COPY ./requirements.txt /requirements.txt
COPY ./app /app

WORKDIR /app
EXPOSE 8000

RUN python3 -m venv /py
RUN /py/bin/pip install --upgrade pip
RUN apk add --update --no-cache postgresql-client && \
    apk add --update --no-cache --virtual .tmp-deps \
        build-base postgresql-dev musl-dev 
RUN /py/bin/pip install -r /requirements.txt
RUN apk del .tmp-deps
RUN addgroup -g $USER_ID $GROUP_NAME && \
    adduser --shell /sbin/nologin --disabled-password \
    --no-create-home --uid $USER_ID --ingroup $GROUP_NAME $USER_NAME
RUN mkdir -p /vol/web/static
RUN mkdir -p /vol/web/media 
RUN chown -R app:appGroup /vol 
RUN chmod -R 755 /vol

ENV PATH="/py/bin:$PATH"

USER app

