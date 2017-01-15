# -*- coding: utf-8 -*-
from tornado import gen

from guitar import exc
from . import route
from .base import BaseHandler


@route('/api')
class UserHandler(BaseHandler):
    @gen.coroutine
    def get(self):
        a = []
        for i in range(10):
            a.append({i: 'a'})

        # raise exc.APIRequestError
        self.write_data(a)
