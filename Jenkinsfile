pipeline {
    agent { label 'linux' }

    environment {
        AWS_CREDENTIALS_ID = 'your-aws-credentials-id' // Replace with your Jenkins credentials ID
        IMAGE_NAME = 'cicd-tests'
        DOCKER_USER = 'lroquec'
        UNIQUE_TAG = "${env.BUILD_NUMBER}"
        TRIVY_IMAGE = 'aquasec/trivy:latest'
        SELENIUM_IMAGE = 'selenium/standalone-chrome:latest' // Official Selenium image with Chrome
        NETWORK_NAME = 'test-network'
        TEST_CONTAINER_IMAGE = 'python:3.13.0-alpine3.20'
    }

    stages {
        stage('SCM checkout') {
            steps{
              git branch: 'main', url: 'https://github.com/lroquec/cicd-jenkins-ec2.git'
              
            }
        }
        stage('Build Docker Image') {
            steps {
                sh 'docker build -t ${DOCKER_USER}/${IMAGE_NAME}:${UNIQUE_TAG} .'
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
               sh "docker run --rm -d --name myapp --network ${NETWORK_NAME} ${IMAGE_NAME}:${UNIQUE_TAG}"

               // Verificar si el contenedor 'selenium' ya está corriendo
               sh 'docker ps --filter "name=selenium" | grep -q . || docker run --rm -d --name selenium --network ${NETWORK_NAME} -p 4444:4444 ${SELENIUM_IMAGE}'
              }
           }
        }

        stage('End-to-End Testing with Selenium') {
            steps {
                script {
                    // Run the test container connected to the same network
                    sh '''
                        docker run --rm --network ${NETWORK_NAME} \
                        -v $(pwd):/app -w /app ${TEST_CONTAINER_IMAGE} \
                        bash -c "pip install pytest selenium && export SELENIUM_URL='http://selenium:4444/wd/hub' && python3 -m pytest tests/ -s --junitxml=report.xml"
                    '''
                }
            }
        }

        stage('Tear Down Containers') {
            steps {
                script {
                    sh 'docker stop myapp selenium'
                    sh 'docker rm myapp selenium'
                    sh 'docker network rm ${NETWORK_NAME} || true'
                }
            }
        }
}
}