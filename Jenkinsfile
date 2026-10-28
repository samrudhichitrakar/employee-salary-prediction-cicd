pipeline {
    agent any
    stages {
        stage('Checkout') {
            steps { checkout scm }
        }
        stage('Install Dependencies') {
            steps {
                bat 'python -m pip install --upgrade pip'
                bat 'pip install -r requirements.txt'
            }
        }
        stage('Test') {
            steps { bat 'python -m pytest -q' }
        }
        stage('Build Docker Image') {
            steps { bat 'docker build -t employee-salary-prediction:latest .' }
        }
    }
}
