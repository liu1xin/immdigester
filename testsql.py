# -*- coding:utf-8 -*-

import datetime
from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session

engine = create_engine("mysql+pymysql://root:root@localhost:29998/test", echo=False)

# 必须使用scoped_session，域session可以将session进行共享
DBSession = scoped_session(sessionmaker(bind=engine))

BaseModel = declarative_base()


# ----------- Relation Model Object---------------- #

class User(BaseModel):

    __tablename__ = "user"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    created_at = Column(DateTime, default=datetime.datetime.now)
    updated_at = Column(DateTime, default=datetime.datetime.now)


class UserCredits(BaseModel):

    __tablename__ = "user_credits"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer)
    user_name = Column(String)
    score = Column(Integer)
    created_at = Column(DateTime, default=datetime.datetime.now)
    updated_at = Column(DateTime, default=datetime.datetime.now)

# ----------- Service implements---------------- #


def add_user(user):
    " 添加用户 "
    session = DBSession()
    
    with session.begin(subtransactions=True):
        session.add(user)
    '''
    try:
        session.add(user)
        session.commit()
    except Exception as e:
        session.rollback()
        print("AddUser: ======={}=======".format(e))
    finally:
        if not session:
            session.close()
    '''

def add_user_credits(userCredits, interrupt=True):
    " 添加用户积分记录 "
    session = DBSession()

    with session.begin(subtransactions=True):
        session.add(userCredits)
"""try:
        if interrupt:
            raise Exception("--- interrupt ---")

        session.add(userCredits)
        session.commit()
    except Exception as e:
        session.rollback()
        print("AddUserCredits: ======={}=======".format(e))
    finally:
        if not session:
            session.close()
"""

def regist_user():

    session = DBSession()
    try:
        # 开启子事务
        #session.begin()

        # TODO Service
        user = User(name='wangzhiping')
        add_user(user)

        with session.begin(subtransactions=True):
            user = session.query(User).one()

        add_user_credits(UserCredits(
            user_id=user.id,
            user_name=user.name,
            score=10
        ), False)

        #session.commit()
    except Exception as e:
        session.rollback()
        print("AddUserCredits: ======={}=======".format(e))
    finally:
        if not session:
            session.close()

# ---------- exec -----------
regist_user()

