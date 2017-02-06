# -*- coding: utf-8 -*-
from sqlalchemy import Column, String, Integer

from . import Base


class UserModel(Base):

    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    username = Column(String(20))
    password = Column(String(256))
    sex = Column(String(10))
    age = Column(Integer)

    def to_json(self):
        return dict(
            username=self.username,
            password=self.password,
            sex=self.sex,
            age=self.age
        )
