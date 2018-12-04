import os
from os import path

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.engine import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session, Session as _Session


ModelBase = declarative_base()
Session = _Session

from DBModel.Record import Record
from DBModel.User import User, createDefaultUser


def init(connect_url, debug=False):
    global Session
    # 释放Session
    if isinstance(Session, scoped_session):
        Session.session_factory.close_all()
        Session = None

    # 连接数据库
    engine = create_engine(connect_url, echo=debug)
    session = sessionmaker(engine)
    Session = scoped_session(session)

    # 创建数据表
    ModelBase.metadata.create_all(engine)

    # 创建默认用户
    sess = Session()
    try:
        createDefaultUser(sess)
    finally:
        sess.close()


with open(path.join(path.dirname(path.abspath(__file__)), "db_uri")) as fp:
    uri = fp.read().strip()
    init(uri)
