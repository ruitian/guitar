# -*- coding: utf-8 -*-
import sqlalchemy as db
from sqlalchemy.orm import relationship, backref

from . import Base
from .relations import UserTag


class UserModel(Base):

    __tablename__ = 'as_user'
    id = db.Column(db.Integer, primary_key=True)
    # 用户唯一的ApeSo账号
    uid = db.Column(db.String(10), index=True, unique=True)
    openid = db.Column(db.String(128), index=True)
    nickname = db.Column(
        db.String(64), index=True, unique=True)
    password = db.Column(db.String(256))
    email = db.Column(db.String(256), index=True, unique=True)
    phone_number = db.Column(db.String(11), index=True, unique=True)
    avatar_url = db.Column(db.Text)  # 头像
    registered_on = db.Column(
        db.TIMESTAMP, index=True,
        server_default=db.func.current_timestamp())
    confirmed = db.Column(db.Boolean, default=False, nullable=False)
    confirmed_on = db.Column(
        db.TIMESTAMP, index=True, default=None, nullable=True)
    # 绑定学生信息
    is_bind_school = db.Column(db.Boolean, default=False, index=True)
    userinfo = relationship('UserinfoModel', backref=backref('user'))

    # tag 标签
    tags = relationship(
        'UserTag',
        foreign_keys=[UserTag.user_id],
        backref=backref('users', lazy='joined'),
        lazy='dynamic',
        cascade='all, delete-orphan')

    def to_dict(self):
        return dict(
            id=self.id,
            uid=self.uid,
            openid=self.openid,
            nickname=self.nickname,
            email=self.email,
            phone_number=self.phone_number,
            avatar_url=self.avatar_url,
            registered_on=self.registered_on,
            confirmed=self.confirmed,
            is_bind_school=self.is_bind_school,
            confirmed_on=self.confirmed_on
        )
