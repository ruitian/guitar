# -*- coding: utf-8 -*-
from . import BaseService
from guitar.models import (UserinfoModel, UserModel)


class StudentService(BaseService):

    def save_student_info(self, user_id, student):
        user = self.session.query(UserModel).filter(
            UserModel.uid == user_id).first()
        student_info = self.session.query(UserinfoModel).filter(
            UserinfoModel.user==user).first()
        if student_info is None:
            info = UserinfoModel(
                number=student['lbl_xh'].encode('utf8'),
                student_name=student['lbl_xm'].encode('utf8'),
                school=u'山东理工大学'.encode('utf8'),
                acachemy=student['lbl_zymc'].encode('utf8'),
                user=user
            )
            try:
                self.session.add(info)
                self.session.commit()
            except:
                self.session.rollback()
            else:
                return True
