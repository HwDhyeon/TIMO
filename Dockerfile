FROM python:3.8.1
USER root
WORKDIR /usr/src

COPY . .

RUN pip install -r requirements.txt
