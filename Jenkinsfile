pipeline {
    agent any
    environment {
        DOCKER_IMAGE = "app-app"
    }
    stages {
        stage('Cloning Repository') {
            steps {
                script {
                    sh 'rm -rf app'
                    sh 'git clone -b main https://github.com/Ciro-Gallucci/Python-Flask-CRUD-App.git app'
                }
            }
        }
        
        stage('Check Docker & Docker Compose') {
            steps {
                script {
                    sh 'docker --version'
                    sh 'docker-compose --version'
                }
            }
        }
        
        stage('Building Docker Images') {
            steps {
                dir('app') {  // Usa il percorso relativo 'app'
                    script {
                        sh 'docker-compose down --rmi all --volumes --remove-orphans'
                        sh 'docker-compose build'
                    }
                }
            }
        }
        
        stage('Starting Containers') {
            steps {
                dir('app') {  // Usa il percorso relativo 'app'
                    script {
                        sh 'docker rm -f flask_crud_app || true'
                        sh 'docker rm -f flask_mysql_db || true' 
                        sh 'docker-compose up -d'
                    }
                }
            }
        }
        
        stage('Waiting for App') {
            steps {
                script {
                    sleep 10 // Attendi un po' per il bootstrap dei container
                    sh 'docker ps'
                }
            }
        }
        
        stage('Check Running Containers') {
            steps {
                dir('app') {  // Usa il percorso relativo 'app'
                    script {
                        sh 'docker-compose ps'
                    }
                }
            }
        }
    }
    post {
        always {
            dir('app') {  // Usa il percorso relativo 'app'
                script {
                    sh 'docker-compose logs'
                }
            }
        }
        failure {
            script {
                echo 'Pipeline fallita! Verifica i log sopra.'
            }
        }
    }
}
