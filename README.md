# Jenkins Demo Pipeline

## Purpose

- Run Jenkins in Docker - `./jenkins-docker/master` and `./docker-compose.ci.yml`
    - Attach build nodes as seperate containers - `./jenkins-docker/slave`
- Run Jenkinsfile pipeline on our app - `./src`
    - pylint, pytest, etc. - `./Jenkinsfile`
    - Build image of our app and push to custom registry - `./Dockerfile.app`
- Run custom Docker Registry - `./docker-compose.registry.yml`

## How to Run

First, we need to start the local Docker Registry:

```bash
# start local docker registry at localhost:5000
docker-compose -f ./docker-compose.registry.yml up
```

Then we need `jenkins-master` and `jenkins-slave` images in our custom registry.

#### Prepare Master Image

```bash
# build Jenkins master image and push to local registry
pushd jenkins-docker/master
docker build -t jenkins-master .
docker tag jenkins-master:latest localhost:5000/jenkins-master:latest
docker push localhost:5000/jenkins-master:latest
popd
```

#### Prepare Slave Image

```bash
# build Jenkins slave image and push to local registry
pushd jenkins-docker/slave
docker build -t jenkins-slave .
docker tag jenkins-slave:latest localhost:5000/jenkins-slave:latest
docker push localhost:5000/jenkins-slave:latest
popd
```

#### Start Jenkins

```bash
# pull local master and slave images and run
docker-compose -f ./docker-compose.ci.yml up
```

## Setup a Pipeline

When Jenkins is ready, visit http://localhost:8080/ to setup your first job. The default admin credentials are `admin:admin`. Create a "Pipeline" with any name. Configure your Jenkinsfile to pull from SCM and provide credentials if necessary.

The `jenkins-slave` we built & ran before will already be connected to `jenkins-master`
as a build node by this point. Visit http://localhost:8080/manage/computer/ to manage
connected nodes.

Once your Pipeline is setup, press the "Build Now" action in the sidebar to kick off the
first build process. It will begin executing steps from within `Jenkinsfile` which is
currently configured to lint code, run unit tests, build an image from `Dockerfile.app`
and then push that image to our local registry as `demo-app:$BUILD_NUMBER`.

You can confirm the entire pipeline completed by checking http://localhost:5000/v2/_catalog
to confirm that `demo-app`, `jenkins-master`, and `jenkins-slave` are available in the
local registry.