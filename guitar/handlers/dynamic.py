# -*- coding: utf-8 -*-
from . import route
from .. import vld
from .base import BaseHandler
from guitar import config
from guitar.services import StudentService
from guitar.services import DynamicService

import requests
import base64
import shutil
from lxml import html
from random import randint
from tornado.web import authenticated


@route('/api/dynamic')
class GetMyDynamicHandler(BaseHandler):

    def initialize(self):
        self.dynamic_service = DynamicService(self.application.session())

    @authenticated
    def get(self):
        offset = self.get_argument('offset', 0)
        limit = self.get_argument('limit', 10)
        user = self.get_current_user()
        dynamics = self.dynamic_service.get_my_dynamic(user['uid'], offset, limit)
        self.write_data(dynamics)