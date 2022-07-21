FROM python:3.9 AS py3
FROM jenkins/jenkins:2.346.2-jdk11

ENV PYTHONUNBUFFERED 1

WORKDIR /app

USER root

RUN apt-get update && apt-get install -y lsb-release

RUN curl -fsSLo /usr/share/keyrings/docker-archive-keyring.asc \
  https://download.docker.com/linux/debian/gpg
RUN echo "deb [arch=$(dpkg --print-architecture) \
  signed-by=/usr/share/keyrings/docker-archive-keyring.asc] \
  https://download.docker.com/linux/debian \
  $(lsb_release -cs) stable" > /etc/apt/sources.list.d/docker.list

RUN apt-get update && apt-get install -y docker-ce-cli python3-pip

USER jenkins
ENV PATH "/var/jenkins_home/.local/bin:${PATH}"

COPY requirements.txt .
RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.txt
COPY . .

RUN jenkins-plugin-cli --plugins "blueocean:1.25.5 docker-workflow:1.28"