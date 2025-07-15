pipeline {
    agent any
    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }
        stage('Hello') {
            steps {
                echo 'Jenkinsfile is working!'
            }
        }
	stage('Backend Lint') {
            steps {
                dir('backend') {
                    sh 'pip install -r requirements.txt'
                    sh 'flake8 .'
                }
            }
        }
    }
}
