FROM python:3.8.1
USER root
WORKDIR /usr/src/TIMO
ENV PYTHONPATH=/usr/src/TIMO/timo;${PYTHONPATH}

COPY . .

RUN apt update && apt upgrade -y
RUN pip install -r requirements.txt
