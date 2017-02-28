# -*- coding: utf-8 -*-


class route(object):

    _routes = []

    def __init__(self, uri):
        self.uri = uri

    def __call__(self, _handler):
        self.__class__._routes.append((self.uri, _handler))
        return _handler

    @classmethod
    def get_routes(cls):
        return cls._routes

from .base import BaseHandler


@route('/')
class IndexHandler(BaseHandler):

    def get(self):
        self.render('dist/index.html')

from . import user  # noqa
