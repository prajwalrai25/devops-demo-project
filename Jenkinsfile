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
                sh '''
                  python -m venv .venv
                  .venv/bin/pip install --no-cache-dir -r app/requirements.txt
                  .venv/bin/pip install --no-cache-dir pytest
                  .venv/bin/pytest
                 '''
            }
        }

        stage('Docker Build') {
            steps {
                sh 'docker build -t devops-demo-app:${BUILD_NUMBER} .'
            }
        }
    }
}
