pipeline {
    agent any

    stages {
        stage('Lint') {
            steps {
                withEnv(["HOME=${env.WORKSPACE}"]) {
                    sh 'pip3.9 install -r src/requirements.txt'
                    sh 'python3.9 -m pylint $(git ls-files "src/**/*.py") --exit-zero'
                }
            }
        }

        stage('Test') {
            steps {
                withEnv(["HOME=${env.WORKSPACE}"]) {
                    sh 'python3.9 -m pytest src/tests'
                }
            }
        }

        stage('Build image') {
            steps {
                sh 'docker build -t demo-app:$BUILD_NUMBER -f Dockerfile.app .'
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
