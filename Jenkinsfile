pipeline {
    agent any
    environment {
        DOCKER_HUB_REGISTRY = 'https://registry.hub.docker.com'
        DOCKER_HUB_CREDENTIALS = 'DockerHub'
        IMAGE_NAME = "nidhishbhimrajka/fair-rent-split"
        IMAGE_TAG = "latest"
        KUBECONFIG = credentials('configfile')
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
                    docker.withRegistry('', DOCKER_HUB_CREDENTIALS) {
                        dockerImage.push()
                    }
                }
            }
        }
        stage('Remove old deployment') {
            steps {
                withKubeConfig([credentialsId: 'configfile']) {
                    sh 'kubectl delete deployment my-app --ignore-not-found=true'
                    sh 'kubectl delete service my-app --ignore-not-found=true'
                }
            }
        }
        stage('Deploy using ansible'){
            steps{
                ansiblePlaybook colorized: true, disableHostKeyChecking: true, installation: 'Ansible', inventory: 'inventory.yaml', playbook: 'playbook.yaml', extras: "-e 'kubeconfig_file=${KUBECONFIG}'"
            }
        }
        stage('Test the Flask Application'){
            steps{
                sh 'pip3 install -r requirements.txt'
                sh 'python3 -m pytest'
            }
        }
    }
}
