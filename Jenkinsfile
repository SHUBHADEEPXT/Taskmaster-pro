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
                    sh '''
                        python3 -m venv venv
                        . venv/bin/activate
                        pip install --upgrade pip
                        pip install -r requirements.txt
                        flake8 . --exclude venv
                    '''
                }
            }
        }
        stage('Test') {
            steps {
                dir('backend') {
                    sh '''
                        . venv/bin/activate
                        pytest
                    '''
                }
            }
        }
        stage('Build Docker Image') {
            steps {
                script {
                    dockerImage = docker.build('difindoxt/taskmaster-pro-backend:latest', 'backend')
                }
            }
        }
        stage('Push Docker Image') {
            steps {
                withCredentials([usernamePassword(credentialsId: 'dockerhub', usernameVariable: 'DOCKERHUB_USER', passwordVariable: 'DOCKERHUB_PASS')]) {
                    script {
                        sh '''
                            echo $DOCKERHUB_PASS | docker login -u $DOCKERHUB_USER --password-stdin
                            docker push difindoxt/taskmaster-pro-backend:latest
                            docker logout
                        '''
                    }
                }
            }
        }
    }
}
