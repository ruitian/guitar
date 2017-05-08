# -*- coding: utf-8 -*-

import sqlalchemy as db

from . import Base


class UserinfoModel(Base):

    __tablename__ = 'as_user_info'

    id = db.Column(db.Integer, primary_key=True)
    number = db.Column(db.String(15), index=True, unique=True)
    student_name = db.Column(db.String(64), index=True)
    sex = db.Column(db.String(32), nullable=True, default=None)
    school = db.Column(db.String(64), index=True)
    college = db.Column(db.String(128), index=True)
    major = db.Column(db.String(256), index=True)
    student_class = db.Column(db.String(256), index=True)
    identity_card = db.Column(db.String(18), nullable=True, default=None)
    # 微信部分
    access_token = db.Column(db.String(128))
    token_refresh = db.Column(db.String(128))
    city = db.Column(db.String(128))

    user_id = db.Column(db.Integer, db.ForeignKey('as_user.id'))

    def to_dict(self):
        return dict(
            id=self.id,
            school=self.school,
            college=self.college,
            major=self.major,
            student_class=self.student_class,
            number=self.number,
            student_name=self.student_name,
            sex=self.sex,
            identity_card=self.identity_card,
        )
