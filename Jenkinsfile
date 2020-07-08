pipeline {
    agent { dockerfile true }

    options {
        ansiColor('xterm')
        copyArtifactPermission('*')
    }

    stages {
        stage("Initialize") {
            steps {
                sh "python timo/core.py setting json"
            }
        }
        stage("CSW") {
            steps {
                sh "python timo/core.py run CSW"
                sh "python timo/core.py parse CSW"
                recordIssues enabledForFailure: true, aggregatingResults: false, tools: [
                    flake8(pattern: "**/flake8.txt", name: "Python codestyle")
                ]
            }
        }
        stage("Unittest") {
            steps {
                sh "python timo/core.py run Unittest"
            }
        }
        stage("Coverage") {
            steps {
                sh "python timo/core.py run Coverage"
                sh "python timo/core.py parse Coverage"
                cobertura coberturaReportFile: '**/coverage.xml', enableNewApi: true
            }
        }
        stage("E2E") {
            steps {
                sh "python timo/core.py parse E2Etest"
                junit 'selenium.xml'
            }
        }
    }
}
