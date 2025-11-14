pipeline {
    agent any

    stages {

        stage('Build Docker Image') {
            steps {
                echo "Building Docker Image..."
                bat 'docker build -t kubdemoapp2:v1 .'
            }
        }

        stage('Docker Login') {
            steps {
                echo "Logging into Docker Hub..."
                bat 'docker login -u varimallamansa1 -p "Manasa@247"'
            }
        }

        stage('Push Docker Image to Docker Hub') {
            steps {
                echo "Pushing Docker Image to Docker Hub..."
                bat 'docker tag kubdemoapp2:v1 varimallamansa1/sample2:kubeimage2'
                bat 'docker push varimallamansa1/sample2:kubeimage2'
            }
        }

        stage('Deploy to Kubernetes') {
        steps {
        echo "Deploying to Kubernetes..."
        withEnv(['KUBECONFIG=C:\\Users\\MANASA\\.kube\\config']) {
            bat 'kubectl apply -f deployment.yaml --validate=false'
            bat 'kubectl apply -f service.yaml'
        }
    }
}

    }

    post {
        success {
            echo 'Pipeline completed successfully!'
        }
        failure {
            echo 'Pipeline failed. Please check the logs.'
        }
    }
}
