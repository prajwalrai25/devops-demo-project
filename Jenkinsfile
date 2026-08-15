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

        stage('SonarQube Scan') {
              steps {
                 script {
                      def scannerhome = tool 'SonarScanner'
                      withSonarQubeEnv('SonarQube') {
                         sh """
                             ${scannerhome}/bin/sonar-scanner \
                             -Dsonar.projectKey=devops-demo-app \
                             -Dsonar.sources=app
                         """
                      }
                     waitForQualityGate abortPipeline:true
                  }
              }
         }

        stage('Docker Build') {
            steps {
                sh 'docker build -t devops-demo-app:${BUILD_NUMBER} .'
            }
        }
       
       stage('Trivy Scan') {
            steps {
              sh '''
                 docker run --rm \
                 -v /var/run/docker.sock:/var/run/docker.sock \
                 aquasec/trivy:latest image \
                 --severity HIGH,CRITICAL \
                 --ignore-unfixed \
                 --exit-code 1 \
                 devops-demo-app:${BUILD_NUMBER}
               '''
            }
        }
    }
}
