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

_Soon we'll make it available for cloning on Dockerhub._  
_곧 도커허브에서도 만나볼 수 있게 만들겠습니다._
