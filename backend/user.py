from curses.ascii import CR
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, Integer, Boolean, DateTime
from sqlalchemy.orm import session
import datetime

Base = declarative_base()

class USER(Base):
    __tablename__='USER'
    
    id_num = Column(Integer, nullable=False, primary_key=True)
    howmany = Column(Integer)
    nowcheck = Column(Boolean, nullable=False)
    xboundary = Column(Integer,nullable=False)
    yboundary = Column(Integer,nullable=False)

    def __init__(self, check,xbound, ybound):
        # self.howmany = peop
        self.nowcheck = check
        self.xboundary = xbound
        self.yboundary = ybound
        
# 사용자가 한명이긴한데 boundary먼저 설정하면서 사용자가 생성이 되어있는지 확인       
 
class CryDetect(Base):
    __tablename__='CryDetect'
    
    id_num = Column(Integer, nullable=False, primary_key=True)
    sound = Column(Integer,nullable=False)
    result = Column(Integer, nullable=False)
    created_at = Column(DateTime, nullable=False)

    def __init__(self, sound, result, dt):
        self.sound = sound
        self.result = result
        self.created_at = dt
 
def findDetect(db_session,id):
    
    try:
        exist=db_session.query(CryDetect).filter(CryDetect.id_num==id).first()
        
    except:
        db_session.rollback()
        
    finally:
       
        db_session.close()
 
    if exist is None:
        
        return False
    else:
        return True
    
def userCheck(db_session):
    try:
        exist=db_session.query(USER).first()
    except:
        db_session.rollback()
        raise
    finally:
        db_session.close()
    if exist is None:
        return False
    else:
        return True

# 인원수 체크를 적용하는지 알아보는 함수 
def applyCheck(db_session):
    try:
        apply = db_session.query(USER).first()
    except:
        db_session.rollback()
        raise
    finally:
        db_session.close()

    # 인원수 적용 여부를 체크할지 확인 
    if apply is not None:
        if apply.nowcheck :
            return True
        else :
            return False
    return False

# 몇명이 있어야 하는지 알아보는 함수 
def getNumber(db_session):
    try:
        num = db_session.query(USER).first()
    except:
        db_session.rollback()
        raise
    finally:
        db_session.close()

    if num is not None:
        return num.howmany
    else :
        return '0'
    
# 사용자의 위치정보 반환 
def getPosition(db_session):
    try:
        pos = db_session.query(USER).first()
    except:
        db_session.rollback()
        raise
    finally:
        db_session.close()

    if pos is not None:
        return [pos.xboundary, pos.yboundary]
    else :
        return [0,0]

