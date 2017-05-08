# -*- coding: utf-8 -*-
from . import BaseService
from guitar.models import (UserinfoModel, UserModel)


class StudentService(BaseService):

    def save_student_info(self, user_id, student):
        user = self.session.query(UserModel).filter(
            UserModel.uid==user_id).first()
        student_info = self.session.query(UserinfoModel).filter(
            UserinfoModel.user==user).first()
        if student_info is None:
            student_info = UserinfoModel(
                school=u'山东理工大学'.encode('utf8'),
                college=student['lbl_xy'].encode('utf-8'),
                major=student['lbl_zymc'].encode('utf8'),
                student_class=student['lbl_xzb'].encode('utf-8'),
                number=student['lbl_xh'].encode('utf8'),
                student_name = student['lbl_xm'].encode('utf8'),
                user=user
            )
        else:
            student_info.school=u'山东理工大学'.encode('utf8')
            student_info.college=student['lbl_xy'].encode('utf-8')
            student_info.major=student['lbl_zymc'].encode('utf8')
            student_info.number=student['lbl_xh'].encode('utf8')
            student_info.student_name=student['lbl_xm'].encode('utf8')
            student_info.student_class=student['lbl_xzb'].encode('utf8')
        try:
            self.session.add(student_info)
            self.session.commit()
        except Exception, e:
            print e
            self.session.rollback()
        else:
            return True

    def get_student_info(self, uid):
        user = self.session.query(UserModel).filter(
            UserModel.uid==uid).first()
        student_info = self.session.query(UserinfoModel).filter(
            UserinfoModel.user==user).first()
        return student_info.to_dict()