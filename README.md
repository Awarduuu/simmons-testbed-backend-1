# testbed-Backend

## WebSocket
> 테스트베드로부터 데이터를 받아와 데이터를 저장하는 과정입니다.

### Installation
> Clone Repository

    $ git clone git@github.com:simmons-testbed/simmons-testbed-backend.git

> Docker

    $ docker-compose up -d

> Prepare


1. Database

mysql_db 컨테이너에 접속하여 데이터베이스 설정을 완료합니다.
```
$ docker exec -it (db 컨테이너명) /bin/bash
$ mysql
$ source /sql/grafana.sql
```

2. WebSocket

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

3. Local에 설치

일단 node, requirements.txt에 있는 파이썬 패키지, mysql이 설치되어 있어야 합니다.

그 후, mysql에 접속하여 grafana.sql을 실행합니다.

그리고, 2번에 node 실행에 필요한 모듈을 모두 설치 후 socket.js를 실행하면 됩니다.

이때, config.py에서 데이터베이스 연결 부분을 아래와 같이 수정합니다.
```
db = {
    'user'     : 'user',
    'password' : '1234',
    'host'     : 'localhost', // 본인 컴퓨터 데이터베이스로 연결할수 있는 ip 
    'port'     : 3306,
    'database' : 'radar'
}

```

---
## Backend



