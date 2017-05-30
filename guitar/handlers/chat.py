# -*- coding: utf-8 -*-
from . import route
from .. import vld
from .base import BaseHandler

import json
from tornado.web import authenticated
from tornado.websocket import WebSocketHandler


clients = {}

@route('/api/chat')
class SocketHandler(WebSocketHandler):

    def check_origin(self, origin):
        return True

    key = ''
    @vld.define_arguments(
        vld.Field('from', required=True),
        vld.Field('to', required=True)
    )
    def open(self, *args):
        chat_from = self.get_argument('from')
        chat_to = self.get_argument('to')
        self.key = self.generate_key(int(chat_from), int(chat_to))
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

    def on_close(self):
        # 通过key删除
        if self.key in clients:
            clients[self.key].remove(self)
            if len(clients[self.key]) == 0:
                del clients[self.key]