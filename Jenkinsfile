pipeline {
    agent {
        docker {
            image 'python:3.7'
        }
    }

    stages {
        stage('Lint') {
            steps {
                withEnv(["HOME=${env.WORKSPACE}"]) {
                    sh 'pip install -r requirements.txt --user'
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
    }
}