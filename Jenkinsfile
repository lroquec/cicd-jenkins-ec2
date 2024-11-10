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
                    sh 'docker network create ${NETWORK_NAME} || true'
                    sh "docker run -d --name myapp --network ${NETWORK_NAME} ${DOCKER_USER}/${IMAGE_NAME}:${UNIQUE_TAG}"
                    sh 'docker run -d --name selenium --network ${NETWORK_NAME} -p 4444:4444 ${SELENIUM_IMAGE}'
                }
            }
        }

        stage('End-to-End Testing with Selenium') {
            steps {
                script {
                    sh '''
                        pip install pytest selenium
                        export SELENIUM_URL="http://selenium:4444/wd/hub"
                        python3 -m pytest tests/ -s --junitxml=report.xml
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