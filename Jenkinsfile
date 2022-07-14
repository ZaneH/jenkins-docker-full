pipeline {
    agent {
        docker { image 'python:3.7' }
    }

    stages {
        stage('Test') {
            steps {
                withEnv(["HOME=${env.WORKSPACE}"]) {
                    sh 'pip install -r requirements.txt --user'
                    sh 'python -m pytest tests'
                }
            }
        }
    }
}