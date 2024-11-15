pipeline {
    agent { label 'linux' }

    environment {
        IMAGE_NAME = 'cicd-tests'
        DOCKER_USER = 'lroquec'
        UNIQUE_TAG = "${env.BUILD_NUMBER}"
        TRIVY_IMAGE = 'aquasec/trivy:latest'
        SELENIUM_IMAGE = 'selenium/standalone-chrome:latest' // Official Selenium image with Chrome
        NETWORK_NAME = 'test-network'
        TEST_CONTAINER_IMAGE = 'python:3.13.0-alpine3.20'
        DOCKERHUB_CREDENTIALS_ID = 'dockerhub'
    }

    stages {

        stage('lint and unit test') {
            agent {
                docker {
                    image 'python:3.13.0-alpine3.20'
                    args '-u root'
                }
            }
            steps {
                 checkout scm
                 sh '''
                   pip install flake8 flask flask-wtf
                   flake8 app.py
                   python3 -m unittest tests/unit_test_app.py 
                 '''
            }
        }

        stage('SCM checkout') {
            steps{
              git branch: 'main', url: 'https://github.com/lroquec/cicd-jenkins-ec2.git'
            }
        }

        stage('sonarqube') {
            environment {
                scannerHome = tool 'sonarQubeScanner';
            }
            steps {
              withSonarQubeEnv(credentialsId: 'sonartoken', installationName: 'sonartoken') {
                sh "${scannerHome}/bin/sonar-scanner"
              }
            }
        }

        stage('Build Docker Image') {
            steps {
                sh 'docker build -t ${DOCKER_USER}/${IMAGE_NAME}:${UNIQUE_TAG} .'
            }
        }

        stage('Trivy Scan') {
            steps {
                sh "docker run --rm -v /var/run/docker.sock:/var/run/docker.sock ${TRIVY_IMAGE} image ${DOCKER_USER}/${IMAGE_NAME}:${UNIQUE_TAG}"
            }
        }

        stage('Setup Network and Run Containers') {
           steps {
              script {
               // Crear la red de Docker
               sh 'docker network create ${NETWORK_NAME} || true'
               // Verificar si el contenedor 'myapp' está corriendo y eliminarlo si es necesario
               sh 'docker ps -a -q --filter "name=myapp" | grep -q . && docker stop myapp && docker rm myapp || true'
               // Correr el contenedor de la aplicación
               sh "docker run --rm -d --name myapp --network ${NETWORK_NAME} ${DOCKER_USER}/${IMAGE_NAME}:${UNIQUE_TAG}"
               // Verificar si el contenedor 'selenium' está corriendo y eliminarlo si es necesario
               sh 'docker ps -a -q --filter "name=selenium" | grep -q . && docker stop selenium && docker rm selenium || true'
               // Correr el contenedor de Selenium
               sh 'docker run --rm -d --name selenium --network ${NETWORK_NAME} -p 4444:4444 ${SELENIUM_IMAGE}'

              }
           }
        }

       stage('End-to-End Testing with Selenium') {
          steps {
             script {
               // Crear un directorio en el host para almacenar el archivo de reporte
               sh 'mkdir -p reports'
               // Ejecutar el contenedor con un volumen montado para compartir el archivo
               sh '''
                     docker run --rm --network ${NETWORK_NAME} \
                     -v $(pwd):/app -v $(pwd)/reports:/app/reports -w /app ${TEST_CONTAINER_IMAGE} \
                     sh -c "pip install pytest selenium && export SELENIUM_URL='http://selenium:4444/wd/hub' && python3 -m pytest tests/ -s --junitxml=reports/report.xml"
               '''
             }
          }
       }

       stage('Tear Down Containers') {
          steps {
             script {
                 // Detener y eliminar los contenedores solo si están corriendo
                 sh 'docker ps -q --filter "name=myapp" | grep -q . && docker stop myapp || true'
                 sh 'docker ps -q --filter "name=selenium" | grep -q . && docker stop selenium || true'
                // Eliminar la red de Docker
                 sh 'docker network rm ${NETWORK_NAME} || true'
             }
          }
       }

        stage('Push to Docker Hub') {
            steps {
                script {
                    // Login en Docker Hub
                    withCredentials([usernamePassword(credentialsId: "${DOCKERHUB_CREDENTIALS_ID}", usernameVariable: 'DOCKER_USER', passwordVariable: 'DOCKER_PASS')]) {
                        sh 'echo $DOCKER_PASS | docker login -u $DOCKER_USER --password-stdin'
                    }
                    // Hacer push de la imagen
                    sh '''
                      docker push ${DOCKER_USER}/${IMAGE_NAME}:${UNIQUE_TAG}
                      docker tag ${DOCKER_USER}/${IMAGE_NAME}:${UNIQUE_TAG} ${DOCKER_USER}/${IMAGE_NAME}:latest
                      docker push ${DOCKER_USER}/${IMAGE_NAME}:latest
                    '''
                }
            }
        }

        stage('Deploy to EC2') {
            steps {
                sshagent(['sshec2']) {
                    sh """
                    ssh -o StrictHostKeyChecking=no ec2-user@3.94.126.23 \\
                    "docker pull ${DOCKER_USER}/${IMAGE_NAME}:latest && \\
                    docker ps -a -q --filter "name=myapp" | grep -q . && docker stop myapp && docker rm myapp || true && \\
                    docker run -d --name myapp -p 5000:5000 ${DOCKER_USER}/${IMAGE_NAME}:latest"
                    """
                }
            }
        }

    }

}