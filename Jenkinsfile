pipeline {
    agent {
        label 'docker'
    }

    environment {
        // Docker stuff.
        registryRepo = 'registry.rohrbach.xyz/replication:latest'
        registryAddress = 'https://registry.rohrbach.xyz'
        registryCredential = 'rohrbach-registry'
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