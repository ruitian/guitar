# -*- coding: utf-8 -*-
from . import BaseService
from guitar.models import (UserinfoModel, UserModel, DynamicModel)


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