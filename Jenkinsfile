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
        DOCKERHUB_CREDENTIALS_ID = 'dockerhub'
    }

    stages {

        stage('Deploy to EC2') {
            steps {
                sshagent(['sshec2']) {
                    sh '''
                    ssh -o StrictHostKeyChecking=no ec2-user@3.94.126.23 << 'ENDSSH'
                    docker pull ${DOCKER_USER}/${IMAGE_NAME}:latest
                    docker run -d -p 5000:5000 ${DOCKER_USER}/${IMAGE_NAME}:latest
                    ENDSSH
                    '''
                }
            }
        }

    }

}