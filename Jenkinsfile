pipeline {
    agent any
    stages {
        stage('Clona Repository') {
            steps {
                git 'https://github.com/keerti1924/Python-Flask-CRUD-App.git'
            }
        }
        stage('Build Docker Compose') {
            steps {
                sh 'docker-compose up -d --build'
            }
        }
    }
}
