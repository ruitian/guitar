# -*- coding: utf-8 -*-
import logging
from tornado.web import gen
from tornado.httpclient import AsyncHTTPClient, HTTPRequest


@gen.coroutine
def rpc(method, uri, **kwargs):
    method = method.upper()
    if not method and method not in ['GET', 'POST', 'PUT', 'DELETE']:
        raise gen.Return(None)

    http_client = AsyncHTTPClient()

    header = kwargs['header'] if 'header' in kwargs else {}
    data = kwargs['data'] if 'data' in kwargs else None
    request = HTTPRequest(
        url=uri, method=method, headers=header, body=data,
        request_timeout=8, validate_cert=False, follow_redirects=False)
    try:
        response = yield http_client.fetch(request)
    except Exception, e:
        logging.warn(e)
        if hasattr(e, 'response'):
            raise gen.Return(e.response)
    else:
        if response.code == 200:
            raise gen.Return(response)
        else:
            raise gen.Return(None)