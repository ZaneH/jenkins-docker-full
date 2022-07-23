# Jenkins Demo Pipeline

<p align="center"><img src="https://i.imgur.com/lqFbmrL.png" width="475px" /></p>

## Purpose

- Run Jenkins in Docker - `./jenkins-docker/controller` and `./docker-compose.ci.yml`
    - Attach build nodes as seperate containers - `./jenkins-docker/agent`
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

Then we need `jenkins-controller` and `jenkins-agent` images in our custom registry.

#### Prepare Controller Image

```bash
# build Jenkins controller image and push to local registry
pushd jenkins-docker/controller
docker build -t jenkins-controller .
docker tag jenkins-controller:latest localhost:5000/jenkins-controller:latest
docker push localhost:5000/jenkins-controller:latest
popd
```

#### Prepare Agent Image

```bash
# build Jenkins agent image and push to local registry
pushd jenkins-docker/agent
docker build -t jenkins-agent .
docker tag jenkins-agent:latest localhost:5000/jenkins-agent:latest
docker push localhost:5000/jenkins-agent:latest
popd
```

#### Start Jenkins

```bash
# pull local controller and agent images and run
docker-compose -f ./docker-compose.ci.yml up
```

## Setup a Pipeline

When Jenkins is ready, visit http://localhost:8080/ to setup your first job. The default admin credentials are `admin:admin`. Create a "Pipeline" with any name. Configure your Jenkinsfile to pull from SCM and provide credentials if necessary.

The `jenkins-agent` we built & ran before will already be connected to `jenkins-controller`
as a build node by this point. Visit http://localhost:8080/manage/computer/ to manage
connected nodes.

Once your Pipeline is setup, press the "Build Now" action in the sidebar to kick off the
first build process. It will begin executing steps from within `Jenkinsfile` which is
currently configured to lint code, run unit tests, build an image from `Dockerfile.app`
and then push that image to our local registry as `demo-app:$BUILD_NUMBER`.

You can confirm the entire pipeline completed by checking http://localhost:5000/v2/_catalog
to confirm that `demo-app`, `jenkins-controller`, and `jenkins-agent` are available in the
local registry.

## How to Integrate

Integrating this demo with your project shouldn't be too hard as most everything is automated and (currently) up-to-date. Here are my recommendations:

- Modify the `agent/Dockerfile` to fit your Jenkins pipeline. This is currently setup with the `ubuntu:18.04` base image, `python3.9` and `pip3.9`
- Move the `Jenkinsfile` into a seperate repo with the `src/` folder containing your app's code
  - Move `Dockerfile.app` and `.dockerignore` too
- Use the remaining files as your CI repository