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
                // 코드 정적분석 실행
                sh "timo run CSW"
                sh "timo parse CSW"

                // 코드 정적분석 결과 퍼블리싱
                recordIssues enabledForFailure: true, aggregatingResults: false, tools: [
                    flake8(pattern: "**/flake8.txt", name: "Python codestyle")
                ]
            }
        }
        stage("Unittest & Coverage") {
            steps {
                //유닛테스트 실행
                sh "timo run Unittest"
                sh "timo parse Unittest"

                // 코드 커버리지 실행
                sh "timo run Coverage"
                sh "timo parse Coverage"

                // 유닛테스트 결과 퍼블리싱
                publishHTML(
                    [
                        allowMissing: false,
                        alwaysLinkToLastBuild:
                        true, keepAll:
                        true,
                        reportDir: 'Unittest-report',
                        reportFiles: '*.html',
                        reportName: 'Unittest Report',
                        reportTitles: 'Unittest'
                    ]
                )

                // 코드 커버리지 결과 퍼블리싱
                cobertura coberturaReportFile: '**/coverage.xml', enableNewApi: true
            }
        }
        stage("Show build score") {
            steps {
                sh "timo get score"
            }
        }
    }
}
