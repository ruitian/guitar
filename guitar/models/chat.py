# -*- coding: utf-8 -*-
import sqlalchemy as db
from sqlalchemy.orm import relationship, backref

from . import Base


class ChatModel(Base):

    __tablename__ = 'as_chat'
    id = db.Column(db.Integer, primary_key=True)
    user = db.Column(db.Integer)
    who = db.Column(db.Integer)
    create_on = db.Column(
        db.TIMESTAMP, index=True, server_default=db.func.current_timestamp(), nullable=True)
    content = db.Column(db.Text)
    is_read = db.Column(db.Boolean)

    def to_dict(self):
        return dict(
            id=self.id,
            user=self.user,
            who=self.who,
            content=self.content
        )
