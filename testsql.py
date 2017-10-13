# coding:utf-8
from gevent import monkey, sleep, spawn, joinall
monkey.patch_all()

import datetime
from sqlalchemy import Column, Integer, String, DateTime, Numeric, create_engine, VARCHAR, UniqueConstraint
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import sqlalchemy
import time
import random
import logging
import pymysql

logging.basicConfig(
    format='%(asctime)s - %(filename)s - %(module)s '
    '- %(lineno)d  - %(process)d -  (%(threadName)-10s) -'
    '%(levelname)s - %(message)s',
    level=logging.INFO)

logger = logging.getLogger(__name__)

DEFAULT_SCORE = 10
BaseModel = declarative_base()




class PymysqlHelper:

    def __init__(self):
        self.connection = pymysql.connect(
            host='localhost', port=3306, user='root', passwd='password', db='test')
        self.connection.cursor().execute("CREATE TABLE IF NOT EXISTS `test_gevent` "
                                         "(`id` INT(11) NOT NULL  AUTO_INCREMENT ,"
                                         "`ip` VARCHAR(16) NOT NULL UNIQUE,"
                                         "`port` INT(10) NOT NULL,"
                                         "`types` INT(3) NOT NULL,"
                                         "`score` INT(3) NOT NULL,"
                                         "`updatetime` DATETIME NOT NULL ,"
                                         "PRIMARY KEY (`id`),"
                                         "UNIQUE KEY `_ip_port` (`ip`,`port`) )"
                                         "ENGINE = InnoDB DEFAULT CHARSET=utf8mb4;")

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.connection:
            self.connection.close()

    def insert(self, data):
        try:
            with self.connection.cursor() as cursor:
                sql = 'INSERT INTO `test_gevent` (`ip`, `port`, `types`, `score`, `updatetime`) VALUES ("{}", "{}", "{}", "{}", "{}")'.format(
                    data['ip'],
                    data['port'],
                    data['types'],
                    DEFAULT_SCORE,
                    datetime.datetime.utcnow(),
                )
                cursor.execute(sql)
            self.connection.commit()
        except Exception as e:
            logger.error(str(e))



# Directed by Mike Bayer, author of sqlalchemy. Links:https://groups.google.com/forum/#!topic/sqlalchemy/wiAnfZQRHdw


# it means like this (here, I adapt your SqlHelper into a recipe that is
# basically equivalent to the context manager at
# http://docs.sqlalchemy.org/en/latest/orm/session_basics.html#when-do-i-construct-a-session-when-do-i-commit-it-and-when-do-i-close-it)


# engine = create_engine(...)
# sessionmaker = sessionmaker(engine)

# class SqlHelper(object):
#     def __init__(self):
#         self.session = sessionmaker()

#     def __enter__(self):
#         return self

#     def __exit__(self ,type, value, traceback):
#         try:
#             if type:
#                self.session.rollback()
#             else:
#                self.session.commit()
#         finally:
#             self.session.close()

#     def insert(self, object):
#         self.session.add(object)

#     def delete(self, object):
#         self.session.delete(object)

#     # ...


# def run_in_gevent():
#     with SqlHelper() as helper:
#         for item in things_to_do():
#             helper.insert(...)
#             helper.delete(...)
#             # ...

# if __name__ = '__main__':
#     for i in range(num_workers):
#         spawn(run_in_gevent)

#    # .. etc

# Following the guidelines at
# http://docs.sqlalchemy.org/en/latest/orm/session_basics.html#when-do-i-construct-a-session-when-do-i-commit-it-and-when-do-i-close-it:

# "keep the lifecycle of the session separate and external from
# functions and objects that access and/or manipulate database data. "
# - we don't commit() the session in the same place that we are doing
# individual insert(), delete(), select() statements - we should have a
# single transaction surrounding a group of operations.

# "Make sure you have a clear notion of where transactions begin and
# end" - the SqlHelper() is used as a context manager, and that's when
# the transaction starts.  outside the "with:" block, the transaction is
# done.




class Proxy(BaseModel):
    __tablename__ = 'test_gevent'
    id = Column(Integer, primary_key=True, autoincrement=True)
    ip = Column(VARCHAR(16), nullable=False)
    port = Column(Integer, nullable=False)
    types = Column(Integer, nullable=False)
    score = Column(Integer, nullable=False, default=DEFAULT_SCORE)
    updatetime = Column(DateTime(), default=datetime.datetime.utcnow)
    __table_args__ = (UniqueConstraint('ip', 'port', name='_ip_port'),)


engine = create_engine(
            'mysql+pymysql://root:password@localhost/test?charset=utf8', echo=True, pool_size=50, max_overflow=100, pool_recycle=3600)

DB_Session = sessionmaker(bind=engine)
    

class SqlHelper:
    params = {'ip': Proxy.ip, 'port': Proxy.port, 'types': Proxy.types, 'score': Proxy.score}

    def __init__(self):
        
        self.session = DB_Session()
    
    def __enter__(self):

        return self

    def __exit__(self ,type, value, traceback):

        try:
            if type:
                self.session.rollback()
            else:
                self.session.commit()
        finally:
            self.session.close()


    def init_db(self):
        BaseModel.metadata.create_all(self.engine)

    def drop_db(self):
        BaseModel.metadata.drop_all(self.engine)


    def insert(self, value):
        proxy = Proxy(ip=value['ip'], port=value['port'], types=value['types'])
        try:
            self.session.add(proxy)
        except sqlalchemy.exc.IntegrityError as e:
            self.session.rollback()
            logger.error(str(e), exc_info=True)
            self.update({"ip": value['ip'], "port": value['port']},
                        {"score": DEFAULT_SCORE})
            logger.debug("{}:{} has been updated".format(
                value['ip'], value['port']))



    def delete(self, conditions=None):
        if conditions:
            conditon_list = []
            for key in list(conditions.keys()):
                if self.params.get(key, None):
                    conditon_list.append(self.params.get(
                        key) == conditions.get(key))
            conditions = conditon_list
            query = self.session.query(Proxy)
            for condition in conditions:
                query = query.filter(condition)
            try:
                deleteNum = query.delete()
            except Exception as e:
                logger.error(str(e), exc_info=True)

        else:
            deleteNum = 0
        return ('deleteNum', deleteNum)

    def update(self, conditions=None, value=None):

        try:
            if conditions and value:
                conditon_list = []
                for key in list(conditions.keys()):
                    if self.params.get(key, None):
                        conditon_list.append(self.params.get(
                            key) == conditions.get(key))
                conditions = conditon_list
                query = self.session.query(Proxy)
                for condition in conditions:
                    query = query.filter(condition)
                updatevalue = {}
                for key in list(value.keys()):
                    if self.params.get(key, None):
                        updatevalue[self.params.get(key, None)] = value.get(key)
                updatevalue['updatetime'] = datetime.datetime.utcnow()
                updateNum = query.update(updatevalue)
            else:
                updateNum = 0
            return {'updateNum': updateNum}

        except Exception as e:
            logger.error(str(e), exc_info=True)




    def select(self, count=None, conditions=None):

        if conditions:
            conditon_list = []
            for key in list(conditions.keys()):
                if self.params.get(key, None):
                    conditon_list.append(self.params.get(
                        key) == conditions.get(key))
            conditions = conditon_list
        else:
            conditions = []

        try:
            query = self.session.query(Proxy.ip, Proxy.port, Proxy.score)
            if len(conditions) > 0 and count:
                for condition in conditions:
                    query = query.filter(condition)
                
                return query.order_by(Proxy.score.desc(), Proxy.speed).limit(count).all()

            elif count:
                return query.order_by(Proxy.score.desc(), Proxy.speed).limit(count).all()

            elif len(conditions) > 0:
                for condition in conditions:
                    query = query.filter(condition)
                return query.order_by(Proxy.score.desc(), Proxy.speed).all()

            else:
                return query.order_by(Proxy.score.desc(), Proxy.speed).all()

        except Exception as e:
            logger.error(str(e), exc_info=True)


pymysqlhelper = PymysqlHelper()

def pymysqlhelper_insert():
    ip = '.'.join([str(random.randrange(0, 255)) for _ in range(4)])
    port = random.randrange(0, 99999)
    data = {'ip': ip, 'port': port, 'types': 0}
    pymysqlhelper.insert(data)


def insert_data():
    with SqlHelper() as sqlhelper:
        time.sleep(random.randrange(1,10))
        ip = '.'.join([str(random.randrange(0, 255)) for _ in range(4)])
        port = random.randrange(0, 99999)
        data = {'ip': ip, 'port': port, 'types': 0}
        sqlhelper.insert(data)


def update_data():
    with SqlHelper() as sqlhelper:
        ip = "5.85.106.130"
        port = 89950
        data = {'ip': ip, 'port': port}
        value = {"score": 20, "types":3}
        sqlhelper.update(data, value)

def print_helloworld():
    print("hello world")


if __name__ == '__main__':
    
    #sqlhelper.update({'ip': '192.168.1.1', 'port': 80}, {'score': 12})
    #print(sqlhelper.select(1))
    #insert_data()
    while True:
        joinall([spawn(insert_data) for _ in range(5)])
        time.sleep(10)

