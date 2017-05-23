# -*- coding: utf-8 -*-
from . import BaseService
from guitar.models import (PraiseModel, UserModel, DynamicModel)


class DynamicService(BaseService):

    def get_my_dynamic(self, uid, offset, limit):
        user = self.session.query(UserModel).filter_by(
            uid=uid
        ).first()
        dynamics = self.session.query(DynamicModel)\
            .filter_by(user=user)\
            .order_by(DynamicModel.create_on.desc())\
            .offset(offset)\
            .limit(limit)\
            .all()
        for dynamic in dynamics:
            dynamic.img_url = dynamic.img_url.split(',')
            setattr(dynamic, 'praises', len(dynamic.praise))
        return [dynamic.to_dict() for dynamic in dynamics]

    def delete_one_dynamic(self, uid, did):
        user = self.session.query(UserModel).filter_by(
            uid=uid
        ).first()
        dynamic = self.session.query(DynamicModel)\
            .filter_by(user=user, id=did).first()
        try:
            self.session.delete(dynamic)
            self.session.commit()
        except:
            self.session.rollback()
        else:
            return True

    # 获取所有的动态信息
    def get_all_dynamic(self, offset, limit):
        dynamics = self.session.query(DynamicModel)\
            .order_by(DynamicModel.create_on.desc())\
            .offset(offset)\
            .limit(limit)\
            .all()
        for dynamic in dynamics:
            dynamic.img_url = dynamic.img_url.split(',')
            setattr(dynamic, 'praises', len(dynamic.praise))
        return [dynamic.to_dict() for dynamic in dynamics]

    # 动态点赞
    def praise_dynamic(self, uid, did):
        user = self.session.query(UserModel).filter_by(
            id=uid).first()
        dynamic = self.session.query(DynamicModel).filter_by(
            id=did).first()
        # 判断用户第一次点赞
        praise = self.session.query(PraiseModel).filter_by(
            user=user, dynamic=dynamic).first()
        if praise is None:
            praise = PraiseModel(
                user=user,
                dynamic=dynamic
            )
            self.session.add(praise)
            try:
                self.session.commit()
            except:
                self.session.rollback()
            else:
                return True
        else:
            return False

    # 取消点赞
    def cancel_praise(self, uid, did):
        user = self.session.query(UserModel).filter_by(
            id=uid).first()
        dynamic = self.session.query(DynamicModel).filter_by(
            id=did).first()
        praise = self.session.query(PraiseModel).filter_by(
            user=user, dynamic=dynamic).first()
        if praise is not None:
            try:
                self.session.delete(praise)
                self.session.commit()
            except:
                self.session.rollback()
            else:
                return True
        else:
            return False