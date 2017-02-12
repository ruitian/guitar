# -*- coding: utf-8 -*-

import sqlalchemy as db

from . import Base


class UserinfoModel(Base):

    __tablename__ = 'as_user_info'

    id = db.Column(db.Integer, primary_key=True)
    number = db.Column(db.String(15), nullable=False, index=True, unique=True)
    student_name = db.Column(db.String(64), nullable=False, index=True)
    sex = db.Column(db.String(32), nullable=True, default=None)
    school = db.Column(db.String(64), nullable=False, index=True)
    acachemy = db.Column(db.String(256), nullable=False)
    identity_card = db.Column(db.String(18), nullable=True, default=None)

    user_id = db.Column(db.Integer, db.ForeignKey('as_user.id'))

    def to_dict(self):
        return dict(
            id=self.id,
            number=self.number,
            student_name=self.student_name,
            sex=self.sex,
            school=self.school,
            acachemy=self.acachemy,
            identity_card=self.identity_card,
        )
