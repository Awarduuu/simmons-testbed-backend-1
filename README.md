# Testbed-Backend

## Installation
> Clone Repository

    $ git clone git@github.com:simmons-testbed/simmons-testbed-backend.git

> Docker를 이용하여 배포

- develop mode
```
    $ docker-compose up -d
```
- production mode
```
    $ docker-compose -f "docker-compose.prod.yml" up -d
```

## WebSocket
> 테스트베드로부터 데이터를 받아와 데이터를 저장하는 기능을 구현하였습니다.

### Prepare

WebSocket

websocket 컨테이너에 접속해 소켓 통신을 실행하기 전 필요한 모듈을 추가로 설치한 후, socket.js를 실행합니다.
```
$ docker exec -it (websocket 컨테이너명) /bin/bash
$ npm install --save (필요한 모듈명)
$ node socket.js
```
* 참고로 socket.js에 테스트베드 IP, PORT, 사용자명을 입력하고 실행하여야 합니다.
```
var usebtswshost = '';    //  테스트베드 IP입니다.
var usebtswsport = '';    //  테스트베드 port입니다.
var usebtswslocaluserid = '';    //  테스트베드에 등록된 사용자입니다.
```


---
## Backend
> 울음 소리 분류 기능 및 위치 정보 확인 기능을 구현하였습니다.

### Prepare
1. Database

mysql_db 컨테이너에 접속하여 데이터베이스 설정을 완료합니다.
```
$ docker exec -it (db 컨테이너명) /bin/bash
$ mysql
$ source /sql/user.sql
```


___

### Local에 설치

일단 node, websocket 폴더와 backend 폴더의 requirements.txt에 있는 파이썬 패키지, mysql이 설치되어 있어야 합니다.

그 후, mysql에 접속하여 user.sql을 실행합니다.

이후, config.py에서 데이터베이스 연결 부분을 아래와 같이 수정합니다.
```
db = {
    'user'     : 'user',
    'password' : '1234',
    'host'     : 'localhost', // 본인 컴퓨터 데이터베이스로 연결할수 있는 ip 
    'port'     : 3306,
    'database' : 'radar'
}

```

