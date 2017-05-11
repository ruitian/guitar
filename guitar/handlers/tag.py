# -*- coding: utf-8 -*-
from . import route
from .. import vld
from .base import BaseHandler
from guitar import config
from guitar.services import TagService
from guitar.services import UserService

import requests
import base64
import shutil
from lxml import html
from random import randint
from tornado.web import authenticated


@route('/api/tag')
class CreateTagHandler(BaseHandler):

    def initialize(self):
        self.tag_service = TagService(self.application.session())

    @vld.define_arguments(
        vld.Field('tag_name', required=True)
    )
    def post(self):

        tag_name = self.get_argument('tag_name')
        tag = self.tag_service.create_tag(tag_name)
        self.write_data(tag)

    # 所有标签
    def get(self):
        self.write_data(self.tag_service.get_tag())

@route('/api/tag/user')
class UserTagHandler(BaseHandler):

    def initialize(self):
        self.tag_service = TagService(self.application.session())

    # 用户添加标签
    @vld.define_arguments(
        vld.Field('tid', dtype=int, required=True)
    )
    def post(self):
        user = self.get_current_user()
        tid = self.get_argument('tid')
        if self.tag_service.add_tag(user['id'], tid):
            self.write_data({'ret': 0, 'msg': '添加成功'})
        else:
            self.write_data({'ret': -1, 'msg': '添加失败'})

    # 用户删除标签
    @vld.define_arguments(
        vld.Field('tid', dtype=int, required=True)
    )
    def delete(self):
        user = self.get_current_user()
        tid = self.get_argument('tid')
        if self.tag_service.user_delete_tag(user['id'], tid):
            self.write_data({'ret': 0, 'msg': '删除成功'})
        else:
            self.write_data({'ret': -1, 'msg': '删除失败'})

    # 获取用户的所有标签
    def get(self):
        user = self.get_current_user()
        self.write_data(self.tag_service.get_user_all_tags(user['id']))