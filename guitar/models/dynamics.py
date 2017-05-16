# -*- coding: utf-8 -*-
import sqlalchemy as db
from sqlalchemy.orm import relationship, backref

from . import Base


# 用户动态数据表
class DynamicModel(Base):

    __tablename__ = 'as_dynamic'

    id = db.Column(db.Integer, primary_key=True)
    # 动态内容
    content = db.Column(db.Text, nullable=False)
    # 动态图片地址
    img_url = db.Column(db.Text, default=None)
    # 定位地址
    address_name = db.Column(db.Text, default=None)
    address_city = db.Column(db.Text, default=None)

    create_on = db.Column(
        db.TIMESTAMP, index=True, server_default=db.func.current_timestamp(), nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('as_user.id'))

    def to_dict(self):
        return dict(
            id=self.id,
            content=self.content,
            img_url=self.img_url,
            address=self.address,
            create_on=self.create_on
        )