# -*- coding: utf-8 -*-
from . import BaseService
from guitar.models import (UserinfoModel, UserModel)


class StudentService(BaseService):

    def save_student_info(self, user_id, student):
        user = self.session.query(UserModel).filter(
            UserModel.uid == user_id).first()
        user_info = self.session.query(UserinfoModel).filter(
            UserinfoModel.user==user).first()
        userinfo = UserinfoModel(
            number=student['lbl_xh'].encode('utf8'),
            student_name=student['lbl_xm'].encode('utf8'),
            school=u'山东理工大学'.encode('utf8'),
            acachemy=student['lbl_zymc'].encode('utf8'),
            user=user
        )
        self.session.add(userinfo)
        self.session.commit()
