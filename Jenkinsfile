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
                            message: "MM testing"
                        )
                    } catch(e) {
                        currentBuild.result = "FAILURE"
                    }
                }
            }
        }
        stage("Docker image build") {
            steps {
                script {
                    try {
                        docker.build("zacharyr/replication")
                    } catch(e) {
                        currentBuild.result = "FAILURE"
                    }
                }
            }
        }   
    }
}