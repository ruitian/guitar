# -*- coding: utf-8 -*-


class BaseService(object):

    def __init__(self, db_session):
        self.session = db_session


from .user import *
