pipeline {
    agent any
    stages {
        stage('Checkout') {
            steps {
               checkout scm
            }
        }
        stage('Installation Dependancies') {
            steps {
               sh 'pip install -r app/requirements.txt'
               sh 'pip install pytest'
            }
        }
        stage('Unit Test') {
            steps {
               sh 'pytest'
            }
        }
        stage('Docker build') {
            steps {
               sh 'docker build -t devops-demo-project:${BUILD_NUMBER} .'
            }
        }
    }
}
