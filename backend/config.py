# # 데이터베이스 연결 관련 파일 
# db = {
#     'user'     : 'user',
#     'password' : '1234',
#     'host'     : 'mysql_db',
#     'port'     : '3306',
#     'database' : 'simmons_testbed'
# }

# DB_URL = f"mysql+mysqlconnector://{db['user']}:{db['password']}@{db['host']}:{db['port']}/{db['database']}?charset=utf8"


db={
    'user':'root',
    'password':'antman1234',
    'host':'127.0.0.1',
    'port' : '3306',
    'database' : 'simmons_testbed'
}

DB_URL = f"mysql+mysqlconnector://{db['user']}:{db['password']}@{db['host']}:{db['port']}/{db['database']}?charset=utf8" 