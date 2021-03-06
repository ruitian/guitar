# -*- coding: utf-8 -*-
import sqlalchemy as db

from . import Base


# 用户与标签关系表
class UserTag(Base):

    __tablename__ = 'as_user_tag'

    user_id = db.Column(
        db.Integer,
        db.ForeignKey('as_user.id'),
        primary_key=True)
    tag_id = db.Column(
        db.Integer,
        db.ForeignKey('as_tag.id'),
        primary_key=True)

    def to_dict(self):
        return dict(
            user_id=self.user_id,
            tag_id=self.tag_id)


# 用户互相关注关系表
class Follow(Base):

    __tablename__ = 'as_follows'

    follower_id = db.Column(db.Integer, db.ForeignKey('as_user.id'), primary_key=True)
    followed_id = db.Column(db.Integer, db.ForeignKey('as_user.id'), primary_key=True)
    timestamp =  db.Column(
        db.TIMESTAMP, index=True, server_default=db.func.current_timestamp(), nullable=True)
