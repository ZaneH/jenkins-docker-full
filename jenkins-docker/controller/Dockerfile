# Start from the Jenkins base image
FROM jenkins/jenkins:latest

# Install the recommended plugins manually
RUN jenkins-plugin-cli -p git matrix-auth pipeline-stage-view workflow-aggregator docker-workflow blueocean credentials-binding

# Setup Jenkins admin user
ENV JENKINS_USER admin
ENV JENKINS_PASSWORD admin

# Skip the setup wizard
ENV JAVA_OPTS "-Djenkins.install.runSetupWizard=false"

# Start-up scripts to setup number of executors and creating the admin user
COPY executors.groovy /usr/share/jenkins/ref/init.groovy.d/
COPY default-user.groovy /usr/share/jenkins/ref/init.groovy.d/

VOLUME /var/jenkins_home