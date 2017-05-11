# -*- coding: utf-8 -*-
import sqlalchemy as db
from sqlalchemy.orm import relationship, backref

from . import Base
from .relations import UserTag


# 个人标签数据表
class TagModel(Base):

    __tablename__ = 'as_tag'

    id = db.Column(db.Integer, primary_key=True)
    tag_name = db.Column(db.String(128), nullable=False)
    create_on = db.Column(
        db.TIMESTAMP, index=True, server_default=db.func.current_timestamp(), nullable=True)

    users = relationship(
        'UserTag',
        foreign_keys=[UserTag.tag_id],
        backref=backref('tags', lazy='joined'),
        lazy='dynamic',
        cascade='all, delete-orphan')


    def to_dict(self):
        return dict(
            id=self.id,
            tag_name=self.tag_name,
            create_on=self.create_on
        )