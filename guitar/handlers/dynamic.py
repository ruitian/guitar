# -*- coding: utf-8 -*-
from . import route
from .. import vld
from .base import BaseHandler
from guitar.services import DynamicService

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

    @authenticated
    @vld.define_arguments(
        vld.Field('did', dtype=int, required=True)
    )
    def post(self):
        did = self.get_argument('did')
        user = self.get_current_user()
        if self.dynamic_service.delete_one_dynamic(user['uid'], did):
            self.write_data({'ret': 0, 'msg': '删除成功'})
        else:
            self.set_status(400)
            self.write_data({'ret': -1, 'msg': '删除失败'})


# 获取所有的动态信息
@route('/api/dynamic/all')
class GetAllDynamic(BaseHandler):
    def initialize(self):
        self.dynamic_service = DynamicService(self.application.session())

    @authenticated
    def get(self):
        offset = self.get_argument('offset', 0)
        limit = self.get_argument('limit', 15)
        data = self.dynamic_service.get_all_dynamic(offset, limit)
        self.write_data(data)


# 动态点赞
@route('/api/dynamic/praise')
class PraiseDynamic(BaseHandler):

    def initialize(self):
        self.dynamic_service = DynamicService(self.application.session())

    @authenticated
    def post(self):
        user = self.get_current_user()
        dynamic_id = self.get_argument('did')
        if self.dynamic_service.praise_dynamic(user['id'], dynamic_id):
            self.write_data({'ret': 0, 'msg': '已点赞'})
        else:
            self.write_data({'ret': -1, 'msg': '重复点赞'})

    @authenticated
    def delete(self):
        user = self.get_current_user()
        dynamic_id = self.get_argument('did')
        if self.dynamic_service.cancel_praise(user['id'], dynamic_id):
            self.write_data({'ret': 0, 'msg': '已取消'})
        else:
            self.write_data({'ret': -1, 'msg': '取消失败'})