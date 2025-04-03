FROM python:3.10 as app-base

WORKDIR /

COPY ./app /app
COPY ./requirements.txt /requirements.txt
COPY ./.env /.env

RUN pip install --no-cache-dir --upgrade -r /requirements.txt

