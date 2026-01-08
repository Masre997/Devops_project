pipeline {
    agent any

    environment {
        DOCKER_IMAGE = "masre/devops_project"
        // Use build number for versioning
        DOCKER_TAG = "${BUILD_NUMBER}" 
    }

    stages {
        stage('Checkout') {
            steps {
                git branch: 'main', url: 'https://github.com/YOUR_GIT_USER/YOUR_REPO.git'
            }
        }

        stage('Build Docker Image') {
            steps {
                script {
                    // Build the image inside the 'app' directory
                    dir('app') {
                        sh "docker build -t ${DOCKER_IMAGE}:${DOCKER_TAG} ."
                        sh "docker build -t ${DOCKER_IMAGE}:latest ."
                    }
                }
            }
        }

        stage('Push to Docker Hub') {
            steps {
                script {
                    withCredentials([usernamePassword(credentialsId: 'docker-hub-credentials', passwordVariable: 'DOCKER_PASSWORD', usernameVariable: 'DOCKER_USERNAME')]) {
                        sh "echo $DOCKER_PASSWORD | docker login -u $DOCKER_USERNAME --password-stdin"
                        sh "docker push ${DOCKER_IMAGE}:${DOCKER_TAG}"
                        sh "docker push ${DOCKER_IMAGE}:latest"
                    }
                }
            }
        }

        stage('Deploy to Kubernetes') {
            steps {
                withKubeConfig([credentialsId: 'k8s-kubeconfig']) {
                    // Apply the changes to the cluster
                    sh "kubectl apply -f k8s/deployment.yaml"
                    sh "kubectl apply -f k8s/service.yaml"
                    
                    // Force rollout to pick up the new image tag if using :latest
                    sh "kubectl rollout restart deployment/devops-app"
                }
            }
        }
    }
}
