# 데이터베이스 연결 관련 파일 
db = {
    'user'     : 'user',
    'password' : '1234',
    'host'     : 'mysql_db',
    'port'     : 3306,
    'database' : 'grafana'
}

DB_URL = f"mysql+mysqlconnector://{db['user']}:{db['password']}@{db['host']}:{db['port']}/{db['database']}?charset=utf8"