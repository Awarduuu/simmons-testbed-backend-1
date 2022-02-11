from flask import Flask, request, jsonify, session 
from flask_cors import CORS
from user import applyCheck, getNumber, getPosition
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from flask_swagger_ui import get_swaggerui_blueprint
from pymongo import MongoClient


app = Flask(__name__,static_url_path='',static_folder="static") 
app.config['JSON_AS_ASCII'] = False
app.config['SECRET_KEY'] = 'wcsfeufhwiquehfdx'

# mysql
app.config.from_pyfile('config.py')
database = create_engine(app.config['DB_URL'], encoding = 'utf-8', max_overflow = 0)
Session = sessionmaker(database)
db_session = Session()

# mongo
client = MongoClient(host='mongo', port=27017)
db = client['radar']
doc = db['position']

# swagger 설정 
CORS(app)
SWAGGER_URL = '/swagger'
API_URL = '/swagger.json'
swaggerui_blueprint = get_swaggerui_blueprint(

    SWAGGER_URL,
    API_URL,
    config = {
        'app_name':"Drugger"
    }
)

app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)



# 위치 정보 데이터를 바탕으로 결과 확인 
@app.route('/check', methods=['GET'])
def check():
    """
    요청을 보내면 가장 최근의 위치 정보 데이터를 불러와서 boundary와 비교를 수행해 경고 반환 

    - 사용자가 입력한 인원수 기준을 적용할지 확인
    - 적용할 경우 현재 레이더 센서 범위 내에 있는 사람의 수와 입력받은 인원수가 일치하는지 확인
        - 인원수가 일치하지 않을 경우 => '3' 반환 
    - 사용자의 위치와 경계 범위와 비교 수행
        - 사용자의 위치가 범위를 벗어났을 경우 => '2' 반환
        - 사용자의 위치가 범위에서 5 이내에 위치할 경우 => '1' 반환
        - 사용자가 안전 범위내에 위치할 경우 => '0' 반환 

    """

    applyNum = applyCheck(db_session)
    number = doc.find().sort("date", -1)[0] # mongodb에서 가장 최근 기록 불러오기

    if applyNum :
        if getNumber(db_session) != len(number['data']): 
            return '3'
    
    pos = getPosition(db_session)

    for data in number['data']:
        if pos[0]< data['pos_x'] or pos[1]<data['pos_y'] :
            return '2'
        elif pos[0]-data['pos_x']<5 or pos[1]-data['pos_y']<5:
            return '1'
    return '0'


if __name__ == "__main__":
    app.run(port=5000, debug=True, host="0.0.0.0")






