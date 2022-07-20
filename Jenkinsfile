pipeline {
    agent any

    stages {
        stage('Lint') {
            steps {
                withEnv(["HOME=${env.WORKSPACE}"]) {
                    sh 'pip install -r requirements.txt'
                    sh 'python -m pylint $(git ls-files "*.py") --exit-zero'
                }
            }
        }

        stage('Test') {
            steps {
                withEnv(["HOME=${env.WORKSPACE}"]) {
                    sh 'python -m pytest tests'
                }
            }
        }

        stage('Build image') {
            steps {
                sh 'docker build -t demo-app:$BUILD_NUMBER .'
                echo 'Built image'
            }
        }

        stage('Push image') {
            steps {
                sh 'docker tag demo-app:$BUILD_NUMBER host.docker.internal:5000/demo-app:$BUILD_NUMBER'
                sh 'docker push host.docker.internal:5000/demo-app'
            }
        }
    }
}