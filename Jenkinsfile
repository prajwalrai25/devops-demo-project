pipeline {
    agent any

    stages {

        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Unit Test') {
            agent {
                docker {
                    image 'python:3.12-slim'
                    reuseNode true
                }
            }

            steps {
                sh 'pip install --no-cache-dir -r app/requirements.txt'
                sh 'pip install --no-cache-dir pytest'
                sh 'pytest'
            }
        }

        stage('Docker Build') {
            steps {
                sh 'docker build -t devops-demo-app:${BUILD_NUMBER} .'
            }
        }
    }
}
