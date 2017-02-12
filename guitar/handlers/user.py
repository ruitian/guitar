# -*- coding: utf-8 -*-
# from tornado import gen
# from tornado.web import authenticated
from . import route
from .. import vld
from .base import BaseHandler
from guitar.utils.tools import encode_json
from guitar.services import UserService

# from tornado_mail import Mail, Message


@route('/api/accounts')
class UserHandler(BaseHandler):

    def initialize(self):
        self.user_service = UserService(self.application.session())

    def get(self):
        users = self.user_service.get_users()
        return self.write_data(users)


@route('/api/account/register')
class RegisterHandler(BaseHandler):

    def initialize(self):
        self.user_service = UserService(self.application.session())

    @vld.define_arguments(
        vld.Field('nickname', dtype=str, required=True),
        vld.Field('password', required=True),
        vld.Field('email', required=True)
    )
    def post(self):
        user_by_nickname = self.user_service.get_user_with_nickname(
            self.get_argument('nickname'))
        user_by_email = self.user_service.get_user_with_email(
            self.get_argument('email'))
        if user_by_nickname is not None:
            rv = {'msg': '昵称被占用', 'ret': -1000}
        if user_by_email is not None:
            rv = {'msg': '邮箱已经注册', 'ret': -1000}
        if user_by_email is None and user_by_nickname is None:
            rv = self.user_service.create_user(self.arguments)

        self.write_data(rv)


@route('/api/account/login')
class LoginHandler(BaseHandler):

    def initialize(self):
        self.user_service = UserService(self.application.session())

    @vld.define_arguments(
        vld.Field('nickname_or_email', dtype=str, required=True),
        vld.Field('password', required=True)
    )
    def post(self):
        rv = self.user_service.get_one_user(self.arguments)
        if rv is None:
            rv = {'msg': '用户名或密码错误', 'ret': -1001}
            self.set_secure_cookie('flash', 'Login incorrect')
        else:
            self.set_current_user(rv)
            self.write_data(rv)

    def set_current_user(self, user):
        if user:
            self.set_secure_cookie('user', encode_json(user))
        else:
            self.clear_cookie('user')
