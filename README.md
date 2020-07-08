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
docker build -f Dockerfile -t timo:latest .
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

#### How to write db.json

**TIMO**가 데이터베이스와 연동을 하기 위해서는 `data/db.json` 파일이 작성되어 있어야 합니다.  
데이터베이스별 작성 예시는 아래와 같습니다.

```json
{
    "mysql": {
        "host": "127.0.0.1",
        "port": 3306,
        "user": "root",
        "password": "myroot",
        "db": "mydatabase",
        "charset": "utf8"
    },
    "oracle": {
        "host": "127.0.0.1",
        "port": "1521",
        "user": "scott",
        "password": "tiger"
    },
    "mongodb": {
        "host": "127.0.0.1",
        "port": "27017"
    }
}
````

_MariaDB를 사용하는 경우에는 MySQL로 작성해주세요 추후에 분리될 것입니다._

## Command list

`conf` 파일 세팅

``` shell
$ python timo/core.py setting --ext="yaml"
We found new configuration file.
```

### Run test

```shell
$ python ./timo/core.py run --test_name=CSW
Running CSW in now.
Run: flake8 timo/ --ignore=E501 --exclude=__init__.py --output-file=flake8.txt
Out: None
Time spending: 0.74 seconds
```

or `make run test=CSW`

### Parsing test results

```shell
$ python ./timo/core.py parse --test_name=CSW
┌―――――――――┬―――――――――┐
│      key      │     value     │
│―――――――――┼―――――――――│
│    warning    │      51       │
└―――――――――┴―――――――――┘
```

or `make parse test=CSW`

### Insert test result to Database

```shell
$ python ./timo/core.py parse --test_name=CSW --db=mysql --build_number=3
Connecting DB...
Done
Time spending: 0.03 seconds

Sending INSERT query...
Done
Time spending: 0.01 seconds
```

or `make insert test=CSW db=mysql build_number=3`

_**TIMO**가 자동으로 `db.json`파일을 읽어서 DB와 연동한다_
