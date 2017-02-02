# -*- coding: utf-8 -*-
# from tornado import gen
# from tornado.web import authenticated
from guitar.store import conn
from . import route
from .base import BaseHandler
from .. import vld
from guitar.utils.tools import  datetime2timestamp
from guitar.services.user import get_user_id, user_register, check_password


@route('/api/accounts')
class UserHandler(BaseHandler):

    @vld.define_arguments(
        vld.Field('name', dtype=int, default='liming', required=True)
    )

    def get(self):
        get_user_id()
        rv = []

        fields = ['user_id', 'username', 'utime']
        users = list(conn.User.find(fields=fields))
        print self.request.__dict__
        # raise exc.APIRequestError
        for user in users:
            user['utime'] = datetime2timestamp(user['utime'])
        rv.extend(users)
        self.write_data(rv)
        self.finish()


@route('/api/account/register')
class RegisterHandler(BaseHandler):

    @vld.define_arguments(
        vld.Field('username', dtype=str, required=True),
        vld.Field('password', required=True)
    )
    def post(self):
        user = user_register(self.arguments)
        print user


@route('/api/account/login')
class LoginHandler(BaseHandler):

    @vld.define_arguments(
        vld.Field('username', dtype=str, required=True),
        vld.Field('password', required=True)
    )
    def post(self):
        is_login = check_password(self.arguments)
        print is_login
