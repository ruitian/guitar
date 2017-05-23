# -*- coding: utf-8 -*-
import sqlalchemy as db
from sqlalchemy.orm import relationship, backref

from . import Base
from .relations import UserTag


class PraiseModel(Base):

    __tablename__ = 'as_praise'

    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(db.Integer, db.ForeignKey('as_user.id'))
    dynamic_id = db.Column(db.Integer, db.ForeignKey('as_dynamic.id'))
    dynamics = relationship('DynamicModel', backref=backref('praise'))
    create_on = db.Column(
        db.TIMESTAMP, index=True, server_default=db.func.current_timestamp(), nullable=True)

    def to_dict(self):
         return dict(
             id=self.id
         )