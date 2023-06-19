import json
from flask import Flask, request, jsonify, session 
from flask_cors import CORS
from user import applyCheck, getNumber, getPosition, userCheck, findDetect, USER, CryDetect
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from flask_swagger_ui import get_swaggerui_blueprint
from pymongo import MongoClient
from rpi_main.make_prediction import PredictAndReturn
import datetime

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
        'app_name':"simmons"
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

# 바운더리설정하고 사람 인원 설정
@app.route('/setBound',methods=['POST'])
def setBound():
    bound=request.get_json()
    
    if userCheck(db_session):
        user=db_session.query(USER).first()
        user.xboundary=bound['xboundary']
        user.yboundary=bound['yboundary']
        db_session.commit()
    else:
        try:
            new_bd=USER(check=False,xbound=bound['xboundary'],ybound=bound['yboundary'])
            db_session.add(new_bd)
            db_session.commit()
        except: 
            return '500'
    
    db_session.close()
    return '200'
    
 
# 받아올때는 0,1로 true false를 받아오는데 저장되고 출력해보면 true false로 표현돼서 조건문엔 true false, 초기화할땐 1,0으로함
@app.route('/storeNum',methods=['POST'])
def storeNum():
    pnum=request.get_json()
    # newcheck가 0이면 howmany도 0으로 보내달라할것
        
    if userCheck(db_session):
        user=db_session.query(USER).first()
        # print(user.nowcheck,pnum['nowcheck'])
        if pnum['nowcheck']==1: #0->1로 변경 = 센서 체크하세요 라는 의미
            if user.nowcheck==True:
                return '500'
            else:
                user.nowcheck=1
                user.howmany=pnum['howmany']   
                db_session.commit()      
        elif pnum['nowcheck']==0: #1->0로 변경 = 센서 끄세요 라는 의미
            if user.nowcheck==False:
                return '500'
            else:
                user.nowcheck=0
                user.howmany=pnum['howmany']
                db_session.commit()      
        return '200'
       
    else: #바운더리부터
        return '500'
    

@app.route('/cryDetect',methods=['POST'])
def cryDetect():
    # index 0 : 울음, 1 : 코골이, 2 : 웃음소리, 3 : 정적
    # json 에서 sound 범위는 0~3
    ck=request.get_json()
    if 0<=int(ck['sound'])<=3:
        sound=int(ck['sound'])
        ml=["realcry.wav","nosesound.ogg","laugh.wav","silence.wav"]
        
        result=PredictAndReturn(ml[sound])
        #print(result,type(result))
        result=int(result)
        now=datetime.datetime.now()
        now=now.strftime('%Y-%m-%d %H:%M:%S')
        #print(now)
        new_record=CryDetect(sound=sound,result=result,dt=now)
        db_session.add(new_record)
        db_session.commit()
        #print(new_record.id_num)
        dic={"result":200,"new_id":new_record.id_num}
        r=jsonify(dic)
        return r
    else:
        return '500'
    
@app.route('/getDetect',methods=['GET'])
def getDetect():
    find_id=request.args.to_dict()
    ml=["realcry.wav","nosesound.ogg","laugh.wav","silence.wav"]
    if findDetect(db_session,find_id['id']): #id 존재여부
           
        info=db_session.query(CryDetect).filter(CryDetect.id_num==find_id['id']).first()
        
        dic={"id":info.id_num,"result":info.result,"sound":ml[info.sound],"created_at":info.created_at}
        # print(dic)
        dic=jsonify(dic)
        # print(dic)
        return dic
    else:
        return '500' 
    # return '200'

    
       
    
    


if __name__ == "__main__":
    app.run(port=5000, debug=True, host="0.0.0.0")






