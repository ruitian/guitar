# -*- coding: utf-8 -*-
import sqlalchemy as db
from sqlalchemy.orm import relationship, backref

from . import Base


class UserModel(Base):

    __tablename__ = 'as_user'
    id = db.Column(db.Integer, primary_key=True)
    nickname = db.Column(
        db.String(64), index=True, nullable=False, unique=True)
    password = db.Column(db.String(256))
    email = db.Column(db.String(256), index=True, unique=True)
    phone_number = db.Column(db.String(11), index=True, unique=True)
    portrait_url = db.Column(db.Text)  # 头像
    registered_on = db.Column(
        db.TIMESTAMP, index=True,
        server_default=db.func.current_timestamp())
    confirmed = db.Column(db.Boolean, default=False, nullable=False)
    confirmed_on = db.Column(
        db.TIMESTAMP, index=True, default=None, nullable=True)
    userinfo = relationship('UserinfoModel', backref=backref('user'))

    def to_dict(self):
        return dict(
            username=self.username,
            password=self.password,
            sex=self.sex,
            age=self.age
        )
