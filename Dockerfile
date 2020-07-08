# Python3.8.1 이미지 사용 OS: ubuntu
FROM python:3.8.1

# root 유저로 실행
USER root

# /usr/src/app/TIMO 디렉토리를 기본 디렉토리로 설정
WORKDIR /usr/src/app/TIMO

# 소스코드 복사
COPY . .

# import 오류를 막기 위해 TIMO/timo를 PYTHONPATH로 등록
ENV PYTHONPATH=/usr/src/app/TIMO/timo;${PYTHONPATH}

# ubuntu 의존성 패키지 설치
RUN apt update && apt upgrade -y
RUN apt install -y \
    git \
    make \
    sudo

# Python 의존성 패키지 설치
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# 타임존 서울로 변경
RUN sudo ln -sf /usr/share/zoneinfo/Asia/Seoul /etc/localtime
