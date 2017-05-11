# -*- coding: utf-8 -*-

from . import BaseService
from guitar.models import TagModel, UserModel, UserTag


class TagService(BaseService):

    # 创建标签
    def create_tag(self, tag_name):
        tag = TagModel(tag_name=tag_name)
        self.session.add(tag)
        self.session.commit()
        return tag and tag.to_dict()

    # 检查用户是否有该标签
    def is_have_tag(self, uid, tid):
        usertags = self.session.query(TagModel).filter_by(
            user_id=uid).all()
        if str(tid) in [str(usertag.tag_id) for usertag in usertags]:
            return True
        return False

    # 为用户添加标签
    def add_tag(self, uid, tid):
        user = self.session.query(UserModel).filter_by(
            id=uid).first()
        tag = self.session.query(TagModel).filter_by(
            id=tid).first()
        user_tag = UserTag(users=user, tags=tag)
        try:
            self.session.add(user_tag)
            self.session.commit()
        except:
            self.session.rollback()
        else:
            return True

    # 用户删除某标签
    def user_delete_tag(self, uid, tid):
        try:
            user_tag = self.session.query(UserTag).filter_by(
                user_id=uid, tag_id=tid
            ).first()
            self.session.delete(user_tag)
            self.session.commit()
        except:
            self.session.rollback()
        else:
            return True

    # 获取标签
    def get_tag(self):
        tags = self.session.query(TagModel).order_by(
            TagModel.create_on.desc()).all()
        return [tag and tag.to_dict() for tag in tags]

    def get_tag_by_name(self, name):
        tag = self.session.query(TagModel).filter_by(
            tag_name=name)
        return tag and tag.to_dict()

    def get_tag_by_id(self, tags):
        new_tags = []
        for tag in tags:
            tag = self.session.query(TagModel).filter_by(
                id=tag.tag_id).first()
            new_tags.append(tag)
        return new_tags

    def get_user_all_tags(self, uid):
        tags = self.session.query(UserTag).filter_by(
            user_id=uid
        ).all()
        new_tags = self.get_tag_by_id(tags)
        return [tag and tag.to_dict() for tag in new_tags]