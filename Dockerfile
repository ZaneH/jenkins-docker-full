FROM python:3.9 AS py3

ENV PYTHONUNBUFFERED 1

WORKDIR /app

USER root

RUN apt-get update && apt-get install -y lsb-release
RUN apt-get update && apt-get install -y python3-pip

ENV PATH "/var/jenkins_home/.local/bin:${PATH}"

COPY requirements.txt .
RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.txt
COPY . .

ENTRYPOINT ["python3"]
CMD ["csgold_validators.py"]