# Supported testing tools

_This document lists the test tools `TIMO` can analyze._

_이 문서에서는 `TIMO`가 분석할 수 있는 테스트 도구의 목록을 나열합니다._

## Support list

이 문단의 도구들은 본래의 사용 목적을 기준으로 나뉘어져 있습니다.  
만약 `Python Unittest`도구로 `API test`를 진행하는 경우 스테이지의 이름에는 `Unittest`가 포함되어야 합니다.

### Source code static analysis tool

- flake8
- eslint  
  경고: ESLint는 Output format으로 작성해야 합니다.  
  `type`에 **eslint**를 작성하면 작동하지 않습니다.

  작성 예시 (Output format이 `checkstyle`인 경우)

  ```json
  "CSW": {
            "uses": "eslint",
            "with": "default",
            "run": [
                "eslint --ext .js -f checkstyle -o checkstyle-result.xml src/"
            ],
            "report": {
                "type": "checkstyle",
                "path": "checkstyle-result.xml"
            }
        }
  ```

  이 아래로는 지원되는 Output format 목록입니다.

  - checkstyle
  - codeframe
  - compact
  - junit
  - jslint-xml
  - json
  - json-with-metadata

### Unit test tool

- surefire

### Code coverage tool

- coverage
- jacoco

### End to End test tool

- selenium
