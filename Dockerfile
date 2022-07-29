FROM python:3.9-alpine3.13
LABEL maintainer="wiringconnection.com"

ENV PYTHONBUFERED 1
ENV USER_ID=65536
ENV GROUP_ID=65536
ENV USER_NAME=app
ENV GROUP_NAME=appGroup

COPY ./requirements.txt /requirements.txt
COPY ./app /app
COPY ./scripts /scripts

WORKDIR /app
EXPOSE 8000

RUN python -m venv /py 
RUN pip install tk
RUN apk add tk
RUN /py/bin/pip install --upgrade pip && \
    apk add --update --no-cache postgresql-client && \
    apk add --update --no-cache --virtual .tmp-deps \
        build-base postgresql-dev musl-dev linux-headers && \
    /py/bin/pip install -r /requirements.txt && \
    apk del .tmp-deps

RUN addgroup -g $USER_ID $GROUP_NAME && \
    adduser --shell /sbin/nologin --disabled-password \
    --no-create-home --uid $USER_ID --ingroup $GROUP_NAME $USER_NAME

RUN mkdir -p /vol/web/static && \
    mkdir -p /vol/web/media && \
    chown -R app:appGroup /vol && \
    chmod -R 755 /vol && \
    chmod -R +x /scripts

ENV PATH="/scripts:/py/bin:$PATH"

USER app

CMD ["run.sh"]