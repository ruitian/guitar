# -*- coding: utf-8 -*-
from . import route
from .. import vld
from .base import BaseHandler
from guitar import config

import requests
import base64
import shutil
from lxml import html
from random import randint


HOST = '210.44.176.229'

@route('/api/crawl')
class CrawlHandler(BaseHandler):

    def filter_string(self, ss_list):
        ll = []
        for ss in ss_list:
            ll.append(ss.split(u'：')[1])
        return ll

    def get(self):
        headers1 = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.8',
            'Cache-Control': 'max-age=0',
            'Connection': 'keep-alive',
            'Host': HOST,
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/49.0.2623.87 Safari/537.36'
        }
        response = requests.get("http://%s"%HOST, headers=headers1)
        tree = html.fromstring(response.text)

        cookies = response.cookies['ASP.NET_SessionId']
        hidden_input = tree.xpath('//input[@name="__VIEWSTATE"]')
        view_state = hidden_input[0].value

        headers2 = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.8',
            'Cache-Control': 'max-age=0',
            'Connection': 'keep-alive',
            'Cookie': 'ASP.NET_SessionId=%s' % cookies,
            'Host': HOST,
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/49.0.2623.87 Safari/537.36'
        }

        cookies = dict({"ASP.NET_SessionId": cookies})
        code_img = requests.get(
            "http://%s/CheckCode.aspx" % HOST,
            headers=headers2,
            cookies=cookies,
            stream=True
        )
        code_index = randint(10000, 100000)
        path = '%s/%s.aspx' % (self.settings.get('code_temp'), code_index)
        with open(path, 'wb') as f:
            code_img.raw.decode_content = True
            shutil.copyfileobj(code_img.raw, f)
        f = open(path, 'rb')
        img_b64 = base64.b64encode(f.read())

        # 写缓存
        self.application.db_redis.set(img_b64, cookies['ASP.NET_SessionId'])
        self.application.db_redis.set(cookies['ASP.NET_SessionId'], view_state)
        info = {
            'view_state': view_state,
            'code_img': img_b64
        }
        self.write_data(info)

    @vld.define_arguments(
        vld.Field('stu_number', dtype=str, required=True),
        vld.Field('stu_password', dtype=str, required=True),
        vld.Field('check_code', dtype=str, required=True),
        vld.Field('check_b64', dtype=str, required=True)
    )
    def post(self):
        stu_number = self.get_argument('stu_number')
        stu_password = self.get_argument('stu_password')
        check_code = self.get_arguments('check_code')
        check_b64 = self.get_argument('check_b64')
        # 在缓存中获取view_state和cookies
        cookies = self.application.db_redis.get(check_b64)
        view_state = self.application.db_redis.get(cookies)

        # 重组cookie及header
        cookies = dict({'ASP.NET_SessionId': cookies})
        headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.8',
            'Cache-Control': 'max-age=0',
            'Connection': 'keep-alive',
            'Content-Length': '292',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Cookie': 'ASP.NET_SessionId=%s' % cookies['ASP.NET_SessionId'],
            'Host': '210.44.176.229',
            'Origin': 'http://210.44.176.229',
            'Referer': 'http://210.44.176.229/',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.87 Safari/537.36'
        }
        post_data = {
            '__VIEWSTATE': view_state,
            'TextBox1': stu_number,
            'TextBox2': stu_password,
            'TextBox3': check_code,
            'RadioButtonList1': '%D1%A7%C9%FA',
            'Button1': '',
            'hidPdrs': '',
            'hidsc': ''
        }

        req_url = 'http://%s/default5.aspx' % HOST
        target_url = 'http://{0}/xs_main.aspx?xh={1}'.format(HOST, stu_number)
        response = requests.post(req_url, data=post_data, headers=headers, cookies=cookies)
        # 判断登录成功
        if response.url == target_url:
            res = {
                'ret': 0,
                'msg': '绑定成功'
            }
            # 处理成功返回的数据，并将学生信息保存到数据库
            req_info_url = "http://{0}/xscjcx.aspx?xh={1}&xm={2}&gnmkdm=N121605".format(HOST, stu_number, stu_password)
            headers = {
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                'Accept-Encoding': 'gzip, deflate, sdch',
                'Accept-Language': 'zh-CN,zh;q=0.8',
                'Connection': 'keep-alive',
                'Host': HOST,
                'Referer': target_url,
                'Upgrade-Insecure-Requests': '1',
                'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) '
                              'Chrome/47.0.2526.111 Safari/537.36'
            }
            page_response = requests.get(req_info_url, headers=headers, cookies=cookies)
            tree = html.fromstring(page_response.content)
            # 学号
            lbl_xh = tree.xpath('//span[@id="lbl_xh"]/text()')[0]
            # 姓名
            lbl_xm = tree.xpath('//span[@id="lbl_xm"]/text()')[0]
            # 学院
            lbl_xy = tree.xpath('//span[@id="lbl_xy"]/text()')[0]
            # 专业
            lbl_zymc = tree.xpath('//span[@id="lbl_zymc"]/text()')[0]
            # 班级
            lbl_xzb = tree.xpath('//span[@id="lbl_xzb"]/text()')[0]
            lbl_xh, lbl_xm, lbl_xy, lbl_xzb =  self.filter_string([lbl_xh, lbl_xm, lbl_xy, lbl_xzb])
            print lbl_xh, lbl_xm, lbl_xy, lbl_zymc, lbl_xzb
        else:
            res = {
                'ret': -1,
                'msg': '绑定失败，请检查您的输入'
            }

        self.write_data(res)