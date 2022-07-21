pipeline {
    agent any

    stages {
        stage('Lint') {
            steps {
                withEnv(["HOME=${env.WORKSPACE}"]) {
                    sh 'pip3.9 install -r requirements.txt'
                    sh 'python3.9 -m pylint $(git ls-files "*.py") --exit-zero'
                }
            }
        }

        stage('Test') {
            steps {
                withEnv(["HOME=${env.WORKSPACE}"]) {
                    sh 'python3.9 -m pytest tests'
                }
            }
        }

        stage('Build image') {
            steps {
                sh 'docker build -t demo-app:$BUILD_NUMBER -f Dockerfile .'
            }
        }

        stage('Push image') {
            steps {
                sh 'docker tag demo-app:$BUILD_NUMBER localhost:5000/demo-app:$BUILD_NUMBER'
                sh 'docker push localhost:5000/demo-app:$BUILD_NUMBER'
            }
        }
    }
}
