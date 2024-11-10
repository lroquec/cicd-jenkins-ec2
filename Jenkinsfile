pipeline {
    agent any

    stages {
        stage('lint and unit test') {
            agent {
                docker {
                    image 'python:3.13.0-alpine3.20'
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
}
}