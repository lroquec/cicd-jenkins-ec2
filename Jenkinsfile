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
        stage('Trivy Scan') {
            steps {
                sh "docker run --rm -v /var/run/docker.sock:/var/run/docker.sock ${TRIVY_IMAGE} image ${DOCKER_USER}/${IMAGE_NAME}:${UNIQUE_TAG}"
            }
        }
}
}