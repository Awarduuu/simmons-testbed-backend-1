import sys
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, Integer
from sqlalchemy.orm import session
from config import DB_URL

database = create_engine(DB_URL, encoding = 'utf-8', max_overflow = 0)
Session = sessionmaker(database)
db_session = Session()
Base = declarative_base()

class BPM(Base):
    __tablename__='bpm'
    val = Column(Integer, nullable=False)
    time = Column(Integer, nullable=False, primary_key=True)

    def __init__(self, val, time):
        self.val = val
        self.time = time

class ENERGY(Base):
    __tablename__='energy'
    val = Column(Integer, nullable=False)
    time = Column(Integer, nullable=False, primary_key=True)

    def __init__(self, val, time):
        self.val = val
        self.time = time

class HBR(Base):
    __tablename__='hbr'
    val = Column(Integer, nullable=False)
    time = Column(Integer, nullable=False, primary_key=True)

    def __init__(self, val, time):
        self.val = val
        self.time = time

class POS(Base):
    __tablename__='pos'
    pos_x = Column(Integer, nullable=False)
    pos_y = Column(Integer, nullable=False)
    pos_z = Column(Integer, nullable=False)
    time = Column(Integer, nullable=False, primary_key=True)

    def __init__(self, pos_x, pos_y, pos_z, time):
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.pos_z = pos_z
        self.time = time



def getValue(data): 
    data = {"m2m:dbg":{"status":"SUCCESS","message":{"SenMngNo":"000100010000000102","SenDateTime":"20220209163222","SenValue":"[{\"MsgID\":1,\"TargetID\":2,\"PositionX\":3,\"PositionY\":24,\"PositionZ\":0,\"BPM\":140,\"HBR\":353,\"Therm\":0,\"rsv\":0,\"Engergy\":1773,\"Point\":0,\"Type\":0,\"status\":2,\"v1\":0,\"v2\":0,\"y1\":0,\"y2\":0}]"}}}
    
    try:
        bpm = BPM(data['m2m:dbg']['message']['SenValue'].split(',')[5].split(':')[1], int(data['m2m:dbg']['message']['SenDateTime'][:-2]))
        energy = ENERGY(data['m2m:dbg']['message']['SenValue'].split(',')[9].split(':')[1], int(data['m2m:dbg']['message']['SenDateTime'][:-2]))
        hbr = HBR(data['m2m:dbg']['message']['SenValue'].split(',')[6].split(':')[1], int(data['m2m:dbg']['message']['SenDateTime'][:-2]))
        pos = POS(data['m2m:dbg']['message']['SenValue'].split(',')[2].split(':')[1], data['m2m:dbg']['message']['SenValue'].split(',')[3].split(':')[1], data['m2m:dbg']['message']['SenValue'].split(',')[4].split(':')[1], int(data['m2m:dbg']['message']['SenDateTime'][:-2]))
        db_session.add_all([bpm, energy, hbr, pos])
        db_session.commit()
    except:
        db_session.rollback()
        raise
    finally:
        db_session.close()

    print (data) 
    
if __name__ == '__main__': 
    getValue(sys.argv[1])
