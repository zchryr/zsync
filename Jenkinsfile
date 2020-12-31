pipeline {
    agent {
        label 'docker'
    }

    environment {
        // Docker stuff.
        registryRepo = 'zacharyr/replication'
        registryCredential = 'dockerhub'
        dockerImage = ''
    }

    stages {
        stage('Build Docker Image') {
            steps {
                script {
                    dockerImage = docker.build(registryRepo + ":dev")
                }
            }
        }
        stage('Publish Image') {
            steps {
                script {
                    docker.withRegistry('', registryCredential) {
                        dockerImage.push()
                    }
                }
            }
        }
    }

    post {
        always {
            deleteDir()
        }
        success {
            mattermostSend color: 'good', message: "Build Number: $BUILD_NUMBER\nJob Name: $JOB_NAME\nBuild URL: $BUILD_URL", text: "$JOB_NAME Pipeline Passing :)"
        }
        failure {
            mattermostSend color: 'bad', message: "Build Number: $BUILD_NUMBER\nJob Name: $JOB_NAME\nBuild URL: $BUILD_URL", text: "$JOB_NAME Pipeline Failing :("
        }
    }

}