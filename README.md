# TIMO

_`TIMO` stands for `Test integration management tool` and is a tool that performs various tests and collects the results into one result._

_`TIMO`는 `테스트 종합 관리도구`의 약자로 각종 테스트를 수행하고 그 결과를 취합하는 도구입니다._

## Installation

### In Host

Clone this repository  
이 저장소를 클론하십시오

```shell
git clone https://github.com/HwDhyeon/TIMO.git
```

### In Docker

_This is the method we recommend._

Clone this repository and build a Dockerfile.  
먼저 이 저장소를 클론하고 도커파일을 빌드하십시오.

```shell
git clone https://github.com/HwDhyeon/TIMO.git
cd TIMO
docker build -f Dockerfile -t TIMO:latest .
```

## Usege

### Setting

이 프로젝트는 data폴더 안에있는 conf 파일을 읽어서 실행됩니다.  
현재 conf 파일은 세 가지 형태를 지원합니다. 지원하는 목록은 다음과 같습니다.

- yaml
- yml
- json

파일 이름은 반드시 `conf.yaml`(또는 `conf.yml`) 이거나 `conf.json` 이어야 합니다. 아니면 두 가지 파일을 모두 사용할 수도 있습니다. 그 방법은 아래에서 설명하겠습니다.

#### How to use two conf files

이 프로그램은 처음 실행 때 반드시 conf 파일이 어떤 형태인지 지정해주어야 합니다. 당신은 그저 `setting` 명령어를 사용하기만 하면 프로그램이 자동으로 당신의 conf 파일을 탐색하고 찾아낸 파일의 형식을 data 폴더 안의 `configpath.json`에 저장합니다. 그래서 이 파일을 미리 구성해놓고 원하는 타이밍에 파일을 수정한다면 두가지 conf 파일을 사용할 수 있습니다. `configpath.json` 파일의 형태는 다음과 같습니다.

```json
{
    "ConfType": "yaml"
}
```

or json and yml

## Command list

`conf` 파일 세팅

``` shell
$ python timo/core.py setting --ext="yaml"
We found new configuration file.
```

테스트 실행

```shell
$ python timo/core.py run --test_name="E2Etest"
Running E2Etest in now.
Run: python -V
Out: Python 3.8.1
Time spending: 0.07 seconds
```
