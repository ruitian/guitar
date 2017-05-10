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

import json
from guitar.utils.fetch import rpc
from tornado import gen

# 微信配置
APP_ID = 'wx59e1951717fc0bf4'
APP_SECRET = 'fd98eb15684aa9a754be8b92e0ee3137'
REDIRECT_URI = 'http%3a%2f%2f127.0.0.1%3a8080%2fverify'


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

    @tornado.web.authenticated
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

    def get(self):
        self.write_data({'ret': -1, 'msg': '该用户没有登录'})

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
                self.session.update(rv.to_dict())
                self.set_current_user(rv)
                self.session.save()

            else:
                rv = {'msg': '账号还没有激活，请检查邮箱邮件', 'ret': -1002}
        self.write_data(rv)


@route('/api/account/logout')
class LogoutHandler(BaseHandler):

    def post(self):
        self.session.clear()
        self.session.save()
        rv = {'msg': '已登出', 'ret': 0}
        self.write_data(rv)

@route('/api/account/verify')
class TokenHandler(BaseHandler):

    def initialize(self):
        self.user_service = UserService(self.application.session())

    @vld.define_arguments(
        vld.Field('token', dtype=str, required=True)
    )
    def get(self):
        token = self.get_argument('token')
        email = self.user_service.verify_email_token(
            token,
            self.application.settings['secret_key'],
            self.application.settings['password_salt']
            )

        if not email:
            rv = {'msg': '验证链接错误', 'ret': -1003}
        else:
            rv = self.user_service.update_user_state(email)
        self.write_data(rv)


@route('/api/account/user')
class CurrentUserHandler(BaseHandler):

    def initialize(self):
        self.user_service = UserService(self.application.session())

    @tornado.web.authenticated
    def get(self):
        if self.session:
            self.write_data(self.session)
        else:
            self.write_data({'ret': -1, 'msg': '该用户没有登录'})


@route('/api/account/nickname')
class GetUserWithNicknameHandler(BaseHandler):

    def initialize(self):
        self.user_service = UserService(self.application.session())

    @vld.define_arguments(
        vld.Field('nickname', dtype=str, required=True)
    )
    def post(self):
        nickname = self.get_argument('nickname')
        user = self.user_service.get_user_with_nickname(nickname)
        if user is not None:
            return self.write_data(user.nickname)
        else:
            return self.write_data({'ret': -1, 'msg': 'null'})


@route('/api/login')
class LoginProxy(BaseHandler):

    def get(self):
        url = 'https://open.weixin.qq.com/connect/oauth2/authorize?' \
              'appid={0}&redirect_uri={1}&response_type=code&scope=snsapi_userinfo&state=1'.format(
            APP_ID, REDIRECT_URI
        )
        self.set_status(302)
        self.redirect(url)


@route('/verify')
class AccessTokenHandler(BaseHandler):

    def initialize(self):
        self.user_service = UserService(self.application.session())

    # 获取access_token及user_info
    @gen.coroutine
    def get(self):
        weixin_code = self.get_argument('code')

        token_url = 'https://api.weixin.qq.com/sns/oauth2/access_token?' \
              'appid={0}&secret={1}&code={2}&grant_type=authorization_code'.format(
            APP_ID, APP_SECRET, weixin_code
        )

        res = yield rpc('GET', token_url)
        res_data = json.loads(res.body)

        info_url = 'https://api.weixin.qq.com/sns/userinfo?access_token={0}&openid={1}&lang=zh_CN'.format(
            res_data['access_token'], res_data['openid']
        )
        user_info_data = yield rpc('GET', info_url)
        user_info = json.loads(user_info_data.body)
        user_info.update(
            res_data
        )

        # 检查用户是否是第一次登录
        user = self.user_service.get_user_with_openid(user_info['openid'])

        if user is None:
            self.user_service.save_weixin_info(user_info)

        # 成功后初始化session
        rv = self.user_service.get_user_with_openid(user_info['openid'])
        self.session.update(rv.to_dict())
        self.set_current_user(rv)
        self.session.save()

        # 保存信息之后进行跳转
        self.set_status(301)
        self.redirect('http://127.0.0.1:8082')
