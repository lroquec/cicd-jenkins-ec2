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
                sh "docker run --rm ${TRIVY_IMAGE} image ${DOCKER_USER}/${IMAGE_NAME}:${UNIQUE_TAG}"
            }
        }
}
}