pipeline {
    agent any
    environment {
        DOCKER_HUB_REGISTRY = 'https://registry.hub.docker.com'
        DOCKER_HUB_CREDENTIALS = 'DockerHub'
        IMAGE_NAME = "nidhishbhimrajka/fair-rent-split"
        IMAGE_TAG = "${env.BUILD_NUMBER}"
    }
    stages {
        stage('Clone git'){
            steps{
                git url: 'https://github.com/nidh-ish/fair-rent-split.git', branch: 'main'
            }
        }
        stage('Build Docker Image') {
            steps {
                script {
                    dockerImage = docker.build("${IMAGE_NAME}:${IMAGE_TAG}", "-f Dockerfile .")
                }
            }
        }
        stage('Push Docker Image') {
            steps {
                script {
                    docker.withRegistry(DOCKER_HUB_REGISTRY, DOCKER_HUB_CREDENTIALS) {
                        dockerImage.push()
                    }
                }
            }
        }
        stage('Deploy to Kubernetes') {
            steps {
                withKubeConfig([credentialsId: 'configfile']) {
                    sh 'kubectl apply -f deployment.yaml -f service.yaml'
                }
            }
        }
        stage('Apply Ingress Configuration') {
            steps {
                withKubeConfig([credentialsId: 'configfile']) {
                    sh "kubectl apply -f ingress.yaml"
                }
            }
        }
    }
}
