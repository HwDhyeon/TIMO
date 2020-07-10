pipeline {
    agent { dockerfile true }

    options {
        ansiColor('xterm')
        copyArtifactPermission('*')
    }

    stages {
        stage("Initialize") {
            steps {
                sh "timo setting json"
            }
        }
        stage("CSW") {
            steps {
                sh "timo run CSW"
                sh "timo parse CSW"
                recordIssues enabledForFailure: true, aggregatingResults: false, tools: [
                    flake8(pattern: "**/flake8.txt", name: "Python codestyle")
                ]
            }
        }
        stage("Unittest") {
            steps {
                sh "timo run Unittest"
            }
        }
        stage("Coverage") {
            steps {
                sh "timo run Coverage"
                sh "timo parse Coverage"
                cobertura coberturaReportFile: '**/coverage.xml', enableNewApi: true
            }
        }
    }
}
