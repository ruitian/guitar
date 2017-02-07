# -*- coding: utf-8 -*-
# from tornado import gen
# from tornado.web import authenticated
from guitar.store import conn
from . import route
from .. import vld
from .base import BaseHandler
from guitar.utils.tools import datetime2timestamp
from guitar.services.user import get_user_id, user_register, check_password
from guitar.utils.tools import encode_json
from guitar.models import UserModel

import random
import time
import tornado
import tornado.websocket
import logging


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
        # raise exc.APIRequestError
        for user in users:
            user['utime'] = datetime2timestamp(user['utime'])
        rv.extend(users)
        session = self.application.session()
        users = session.query(UserModel).all()
        self.write_data([user.to_json() for user in users])
        self.finish()


@route('/api/account/register')
class RegisterHandler(BaseHandler):

    @vld.define_arguments(
        vld.Field('username', dtype=str, required=True),
        vld.Field('password', required=True)
    )
    def post(self):
        user = user_register(self.arguments)
        rv = {'msg': '用户名已经被占用'}
        if user is not None:
            self.write_data(rv)


@route('/api/account/login')
class LoginHandler(BaseHandler):

    def get(self):
        # 通过cookie测试
        self.render('login.html',
                    notification=self.get_flash(),
                    current_user=self.get_current_user())

    @vld.define_arguments(
        vld.Field('username', dtype=str, required=True),
        vld.Field('password', required=True)
    )
    def post(self):
        is_login, user = check_password(self.arguments)
        if not is_login:
            rv = {'msg': '用户名或密码错误'}
            self.set_secure_cookie('flash', 'Login incorrect')
            # self.redirect('/api/account/login')
            return self.write_data(rv)
        else:
            self.set_current_user(user)
            return self.write_data(user)

    def set_current_user(self, user):
        if user:
            self.set_secure_cookie('user', encode_json(user))
        else:
            self.clear_cookie('user')


@route('/api/account/current')
class CurrentUserHandler(BaseHandler):
    def post(self):
        return self.write_data(self.get_current_user())


@route('/api/test')
class TestHandler(BaseHandler):

    def get(self):
        a = self.render_string('error.html')
        print a
        self.render('index.html', info="下面显示服务端数据")

    @tornado.web.asynchronous
    def post(self):
        self.get_data(callback=self.on_finished)

    def get_data(self, callback):
        if self.request.connection.stream.closed():
            return
        num = random.randint(1, 100)
        tornado.ioloop.IOLoop.instance().add_timeout(
            time.time()+3,
            lambda: callback(num)
        )

    def on_finished(self, data):
        self.write('Server says: %d' % data)
        self.finish()


@route('/ws')
class WebSocketHandler(tornado.websocket.WebSocketHandler):

    def check_origin(self, origin):
        return True

    def open(self):
        for i in range(10):
            num = random.randint(1, 100)
            self.write_message(str(num))

    def on_message(self, message):
        logging.into('getting message' + message)
        self.write_message("You say" + message)
