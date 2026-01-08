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
                git branch: 'main', url: 'https://github.com/Masre997/Devops_project.git'
            }
        }

        stage('Build & Push Docker Image') {
            steps {
                script {
                    withCredentials([usernamePassword(credentialsId: 'docker-hub-credentials', passwordVariable: 'DOCKER_PASSWORD', usernameVariable: 'DOCKER_USERNAME')]) {
                        
                        // 1. CLEAR OLD CREDENTIALS & LOGIN FRESH
                        // We log in BEFORE building to fix the "401 Unauthorized" error on pull
                        sh "docker logout"
                        sh 'echo $DOCKER_PASSWORD | docker login -u $DOCKER_USERNAME --password-stdin'
                        
                        // 2. BUILD THE IMAGE
                        dir('app') {
                            echo "Building Docker Image..."
                            sh "docker build -t ${DOCKER_IMAGE}:${DOCKER_TAG} ."
                            sh "docker build -t ${DOCKER_IMAGE}:latest ."
                        }
                        
                        // 3. PUSH THE IMAGE
                        echo "Pushing to Docker Hub..."
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
