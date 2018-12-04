from sqlalchemy import Column, String, BigInteger, SmallInteger
from sqlalchemy.orm import Session

from DBModel import ModelBase


class User(ModelBase):
    __tablename__ = "t_user"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    username = Column(String(20), unique=True, nullable=False)
    password = Column(String(32), nullable=False)
    permission = Column(SmallInteger, default=0, nullable=False)

    def setPassword(self, pwd: str):
        from hashlib import md5
        self.password = md5(pwd.encode()).hexdigest()


def createDefaultUser(sess: Session):
    """ 创建默认用户, 如果默认用户已经存在, 不会做任何操作, 将会创建以下三个用户
    - user: 普通用户, 只能查看站点状态和站点记录（查看的记录仅包含已确认为黑烟的记录）
    - aduitor: 审核用户, 能查看站点状态和站点记录, 并且能对站点记录进行确认和上传（只能查看未确认的记录）
    - admin: 管理员, 拥有所有功能
    """
    users = [
        User(username="user", password="sfe-123456", permission=0),
        User(username="auditor", password="sfe@123456", permission=1),
        User(username="admin", password="admin@sfe", permission=2)
    ]
    users = {u.username: u for u in users}

    sub_set = {u.username for u in sess.query(User).filter(User.username.in_(users.keys())).all()}
    all_set = set(users.keys())
    for username in all_set-sub_set:
        user = users[username]
        user.setPassword(user.password)
        sess.add(user)
    sess.commit()
