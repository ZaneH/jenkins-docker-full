FROM ubuntu:18.04

# Install Docker CLI in the agent and other deps
RUN apt-get update && apt-get install -y openjdk-11-jre curl python3 python3-pip git
RUN pip3 install python-jenkins
RUN apt-get install -y ca-certificates curl gnupg lsb-release apt-transport-https
RUN mkdir -p /etc/apt/keyrings
RUN curl -fsSL https://download.docker.com/linux/ubuntu/gpg | gpg --dearmor -o /etc/apt/keyrings/docker.gpg
RUN echo "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" | tee /etc/apt/sources.list.d/docker.list > /dev/null
RUN apt-get update
RUN apt-get install -y docker-ce docker-ce-cli containerd.io docker-compose-plugin docker-compose

RUN mkdir -p /home/jenkins
RUN mkdir -p /var/lib/jenkins

# Start-up script to attach the slave to the master
ADD slave.py /var/lib/jenkins/slave.py
WORKDIR /home/jenkins
ENV JENKINS_URL "http://jenkins"
ENV JENKINS_SLAVE_ADDRESS ""
ENV JENKINS_USER "admin"
ENV JENKINS_PASS "admin"
ENV SLAVE_NAME ""
ENV SLAVE_SECRET ""
ENV SLAVE_EXECUTORS "1"
ENV SLAVE_LABELS "docker"
ENV SLAVE_WORING_DIR ""
ENV CLEAN_WORKING_DIR "true"
CMD [ "python3", "-u", "/var/lib/jenkins/slave.py" ]
