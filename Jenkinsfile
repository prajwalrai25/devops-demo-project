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

        stage('Docker push') {
           steps {
              withCredentials([
                  usernamePassword(
                      credentialsId:'dockerhub-id',
                      usernameVariable:'DOCKER_USERNAME',
                      passwordVariable:'DOCKER_TOKEN'
                  )
              ])
                {
                  sh '''
                      echo "$DOCKER_TOKEN" | docker login \
                       -u "$DOCKER_USERNAME" \
                       --password-stdin
                 
                      docker tag devops-demo-app:${BUILD_NUMBER} \
                      prajj29/devops-demo-app:${BUILD_NUMBER} 
                  
                      docker push prajj29/devops-demo-app:${BUILD_NUMBER}

                      docker logout
                '''
               }

            }
        }
        
       stage('Image digest capture') {
           steps {
              script {
                 env.IMAGE_DIGEST=sh(
                    script: """
                        docker inspect --format='{{index .RepoDigests 0}}' \
                        prajj29/devops-demo-app:${BUILD_NUMBER} \
                     """,
                     returnStdout: true
                 ).trim()
                 
                 echo "Image digest:${env.IMAGE_DIGEST}"
               }
            }
      }
     
     stage("Cosign Image Digest") {
         steps {
           withCredentials([
               usernamePassword(
                   credentialsId:'dockerhub-id',
                   usernameVariable:'DOCKER_USERNAME',
                   passwordVariable:'DOCKER_TOKEN'
               ),
               
               file(
                   credentialsId:'cosign-private-key',
                   variable:'COSIGN_KEY'
               ),
               
              string(
                  credentialsId:'cosign-key-password',
                  variable:'COSIGN_PASSWORD'
              )
           ]) {
               sh '''
                 echo "$DOCKER_TOKEN" | docker login -u "$DOCKER_USERNAME" --password-stdin
                 cosign sign \
                  --key "$COSIGN_KEY" \
                  "$IMAGE_DIGEST"
               '''
              }
         }
     }
  
     stage('Cosign verification') {
         steps {
             withCredentials([
               file(
                 credentialsId:'cosign-public-key'
                 variable:'COSIGN_PUBLIC_KEY'
               )
             ]) {
                  sh '''
                    cosign verify --key "$COSIGN_PUBLIC_KEY" "$IMAGE_DIGEST"
                  '''
                }
         }
     }
             
    }
}
