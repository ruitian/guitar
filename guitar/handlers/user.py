# -*- coding: utf-8 -*-
# from tornado import gen
# from tornado.web import authenticated
from . import route
from .. import vld
from .base import BaseHandler
from guitar.utils.tools import encode_json
from guitar.services import UserService

from urllib import urlencode

import tornado
from tornado_mail import Mail, Message
from tornado.concurrent import Future


@tornado.gen.coroutine
def send_confirm_mail(app, reciver, url):
    future = Future()

    mail = Mail(app)
    msg = Message(
        subject='ApeSo verify account',
        body=url,
        recipients=reciver
    )
    try:
        mail.send(msg)
        future.set_result({'msg': '发送成功!'})
    except Exception, e:
        future.set_result({'msg': '发送失败!'})
        raise e
    return future


@route('/api/accounts')
class UserHandler(BaseHandler):

    def initialize(self):
        self.user_service = UserService(self.application.session())

    def get(self):
        users = self.user_service.get_users()
        self.write_data(users)
        self.finish()


@route('/api/account/register')
class RegisterHandler(BaseHandler):

    def initialize(self):
        self.user_service = UserService(self.application.session())

    @vld.define_arguments(
        vld.Field('nickname', dtype=str, required=True),
        vld.Field('password', required=True),
        vld.Field('email', required=True)
    )
    @tornado.gen.coroutine
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
            token = self.user_service.generate_confirmation_token(
                self.get_argument('email'),
                self.application.settings['secret_key'],
                self.application.settings['password_salt']
            )
            param = {
                'token': token
            }
            url = '{0}{1}{2}{3}'.format(
                'http://', self.request.host,
                '/api/account/verify?', urlencode(param))
            rv = self.user_service.create_user(self.arguments)
            result = yield send_confirm_mail(
                self.application, [self.get_argument('email')], url)
            rv.update(result.result())

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
            self.clear_cookie('user')
            self.set_secure_cookie('flash', 'Login incorrect')
        else:
            if rv.confirmed:
                self.session['nickname'] = rv.nickname
                self.session.save()
                self.set_current_user(rv)
            else:
                rv = {'msg': '账号还没有激活，请检查邮箱邮件', 'ret': -1002}
        print self.session
        self.write_data(rv)

    def set_current_user(self, user):
        if user:
            self.clear_cookie('flash')
            self.set_secure_cookie('user', encode_json(user))
        else:
            self.clear_cookie('user')


@route('/api/account/verify')
class TokenHandler(BaseHandler):

    def initialize(self):
        self.user_service = UserService(self.application.session())

    @vld.define_arguments(
        vld.Field('token', dtype=str, required=True)
    )
    def get(self):
        token = self.get_argument('token')
        email = self.user_service.verify_email_token(token,
                                                     self.application.settings['secret_key'],
                                                     self.application.settings['password_salt']
                                                    )

        if not email:
            rv = {'msg': '验证链接错误', 'ret': -1003}
        else:
            rv = self.user_service.update_user_state(email)
        self.write_data(rv)
