node {
    agent {
        docker {
            image 'host.docker.internal:5000/demo-app'
            registryUrl 'https://host.docker.internal'
            registryCredentialsId 'local-registry'
            args '--entrypoint=""'
        }
    }

    stage('Clone repository') {
        checkout scm
    }

    stage('Build image') {
        docker.build('demo-app-image', '.')
    }

    stage('Test image') {
        docker.image('demo-app-image').inside {
            sh 'pip3 install -r requirements.txt'
            sh 'python3 -m pylint $(git ls-files "*.py") --exit-zero'
        }
    }

    stage("Push image") {
        docker.withRegistry("http://host.docker.internal:5000") {
            demoAppImage.push()
        }
    }
}