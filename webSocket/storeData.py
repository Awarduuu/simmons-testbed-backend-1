from pymongo import MongoClient
import json
import sys

# 본인 컴퓨터의 MongoDB와 연결을 수행한다.
client = MongoClient(host='mongo', port=27017)

# 위치 정보 저장할 데이터베이스
db = client['radar']
# 데이터 베이스 하위에 collection도 불러온다.
mydoc = db['position']

def getValue(): 
    inputs = {"m2m:dbg":{"status":"SUCCESS","message":{"SenMngNo":"000100010000000102","SenDateTime":"20220209163222","SenValue":"[{\"MsgID\":1,\"TargetID\":2,\"PositionX\":3,\"PositionY\":24,\"PositionZ\":0,\"BPM\":140,\"HBR\":353,\"Therm\":0,\"rsv\":0,\"Engergy\":1773,\"Point\":0,\"Type\":0,\"status\":2,\"v1\":0,\"v2\":0,\"y1\":0,\"y2\":0}]"}}}
    datas = json.loads(inputs['m2m:dbg']['message']['SenValue'])
    positions = []
    for data in datas:
        pos = {
            'target' : data['TargetID'],
            'pos_x' : data['PositionX'],
            'pos_y' : data['PositionY']
        }
        positions.append(pos)
    
    data_info = {
        "date" : int(inputs['m2m:dbg']['message']['SenDateTime'][:-2]),
        "data" : positions
    }
    mydoc.insert_one(data_info)
    client.close()

if __name__ == '__main__': 
    #getValue(sys.argv[1])
    getValue()

