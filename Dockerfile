FROM python:3.9 AS py3

ENV PYTHONUNBUFFERED 1

WORKDIR /app

USER root

RUN apt-get update && apt-get install -y python3.9 python3.9-pip

COPY requirements.txt .
RUN pip3.9 install --upgrade pip
RUN pip3.9 install -r requirements.txt
COPY . .

ENTRYPOINT ["python3.9", "csgold_validators.py"]
