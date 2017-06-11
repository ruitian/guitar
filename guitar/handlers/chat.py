# -*- coding: utf-8 -*-
from . import route
from .. import vld
from .base import BaseHandler
from guitar.services import ChatService

import json
from tornado.web import authenticated
from tornado.websocket import WebSocketHandler


clients = dict()
waiters = dict()


@route('/api/chat')
class SocketHandler(WebSocketHandler):

    def initialize(self):
        self.chat_service = ChatService(self.application.session())

    def check_origin(self, origin):
        return True

    key = ''

    @vld.define_arguments(
        vld.Field('from', required=True),
        vld.Field('to', required=True)
    )
    def open(self, *args):
        global id_a
        global id_b
        id_a = chat_from = int(self.get_argument('from'))
        id_b = chat_to = int(self.get_argument('to'))
        self.key = self.generate_key(chat_from, chat_to)
        if self.key in clients:
            clients[self.key].append(self)
        else:
            clients[self.key] = [self]

    def generate_key(self, id_a, id_b):
        min = id_a
        max = id_b
        if min > max:
            max = id_a
            min = id_b
        key = '{0}_{1}'.format(min, max)
        return key

    def on_message(self, message):
        self.send_to_all(message)

    def send_to_all(self, message):
        for chat in clients[self.key]:
            chat.write_message(message)
        self.chat_service.save_chat_record(id_a, id_b, message)
        # 用户不在线
        if str(id_b) not in waiters:
            self.chat_service.save_chat_record(id_a, id_b, message, is_read=False)
        else:
            self.chat_service.save_chat_record(id_b, id_a, message)

    def on_close(self):
        # 通过key删除
        if self.key in clients:
            clients[self.key].remove(self)
            if len(clients[self.key]) == 0:
                del clients[self.key]


@route('/api/chat/record')
class ChatRecordSocket(WebSocketHandler):

    def check_origin(self, origin):
        return True

    def open(self):
        global id
        id = self.get_argument('id')
        waiters[id] = self
        self.send_to_user(id, 'sdf')

    def send_to_user(self, id, message):
        waiters[id].write_message(message)

    def on_close(self):
        waiters.pop(str(id))
        print("WebSocket closed")


@route('/api/chat/unread')
class ChatUnreadHandler(BaseHandler):

    def initialize(self):
        self.chat_service = ChatService(self.application.session())

    @authenticated
    def get(self):
        user = self.get_current_user()
        chat = self.chat_service.get_chat_unread(user['id'])
        self.write_data(chat)

@route('/api/chat/unread/count')
class ChatUnreadCountHandler(BaseHandler):

    def initialize(self):
        self.chat_service = ChatService(self.application.session())

    @authenticated
    def get(self):
        user = self.get_current_user()
        chat = self.chat_service.get_chat_unread_count(user['id'])
        self.write_data({'count': chat})