pipeline {
    agent {
        label 'ubuntu'
    }

    stages {
        stage('echo') {
            steps {
                sh 'echo "Hello world!"'
            }
        }
        stage('mm') {
            steps {
                script {
                    try {
                        mattermostSend (
                            color: "#2A42EE",
                            message: "testing"
                        )
                    } catch(e) {
                        currentBuild.result = "FAILURE"
                    }
                }
            }
        }
    }
}