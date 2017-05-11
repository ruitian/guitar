# -*- coding: utf-8 -*-
import session
from tornado.web import RequestHandler
from raven.contrib.tornado import SentryMixin

from guitar.utils.tools import encode_json, decode_json
from guitar import exc


class BaseHandler(SentryMixin, RequestHandler):
    __return__ = 'json'
    __error_code__ = 400
    __exception_handlers = {
        exc.APIRequestError: '_handle_api_error',
    }

    def __init__(self, *args, **kwargs):
        super(BaseHandler, self).__init__(*args, **kwargs)
        self.session = session.Session(self.application.session_manager, self)

    def _handle_error(self, e):
        d = {
            'code': getattr(e, 'code', 1),
            'msg': str(e)
        }
        code = self.__error_code__
        if self.get_argument('__return_code', None):
            code = int(self.get_argument('__return_code'))
            if code != 200:
                code = 400
        self.write_data(d, code=code, no_wrap=True)

    def _handle_other_error(self, e):
        d = {
            'code': exc.Code.INTERNAL_ERROR[0],
            'msg': exc.Code.INTERNAL_ERROR[1]
        }
        self.write_data(d, code=400, no_wrap=True)

    def _handle_api_error(self):
        d = {
            'code': exc.Code.API_REQUEST_ERROR[0],
            'msg': exc.Code.API_REQUEST_ERROR[1]
        }
        self.write_data(d, code=400, no_wrap=True)

    def write_data(self, data, **kwargs):
        d = data if kwargs.get('no_wrap') else {'data': data}
        if self.__return__ == 'json_as_plain_text':
            if kwargs.get('code'):
                self.set_status(kwargs.get('code'))

            json_str = encode_json(d)
            self.set_header("Content-Type", "text/plain; charset=utf-8")
            self.write(json_str)

        else:
            self.write_json(d,
                            code=kwargs.get('code'),
                            headers=kwargs.get('headers'))

    def write_json(self, data, code=None, headers=None):
        chunk = encode_json(data)

        self.set_header('Content-Type', 'application/json; charset=UTF-8')
        if code:
            self.set_status(code)
        if headers:
            for k, v in headers.iteriterms():
                self.set_header(k, v)

        self.write(chunk)

    def get_current_user(self):
        return self.session

    def get_cookie_user(self):
        return self.get_secure_cookie('user')

    def get_flash(self):
        flash = self.get_secure_cookie('flash')
        self.clear_cookie('flash')
        return flash

    # def set_current_user(self, user):
    #     if user:
    #         self.clear_cookie('flash')
    #         self.set_secure_cookie('user', encode_json(user))
    #     else:
    #         self.clear_cookie('user')

    def =(self, user):
        self.session.update(user.to_dict())
        self.session.save()