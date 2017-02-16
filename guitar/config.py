# -*- coding: utf-8 -*-
import os  # noqa
import uuid
import base64


class config:

    MONGODB_REPLICASET = ''
    MONGODB_HOST = '127.0.0.1'
    MONGODB_PORT = 27017
    MONGODB_DB = 'guitar'
    MONGODB_USER = ''
    MONGODB_PWD = ''

    MONGODB_MAX_POOL_SIZE = 10
    MONGODB_CONNECT_TIMEOUT_MS = 1000
    MONGODB_SOCKET_TIMEOUT_MS = 10000
    MONGODB_WAIT_QUEUE_TIMEOUT_MS = 6000
    MONGODB_WAIT_QUEUE_MULTIPLE = 5000

    # redis
    # redis 配合session
    REDIS_STORE = {
        'redis_host': '127.0.0.1',
        'redis_port': 6379,
        'redis_pass': ''
    }

    COOKIE_SECRET = base64.b64encode(uuid.uuid4().bytes + uuid.uuid4().bytes)
    SESSION_SECRET = base64.b64encode(uuid.uuid4().bytes + uuid.uuid4().bytes)
    SESSION_TIMEOUT = 60
    TEMPLATE_PATH = os.path.join(os.path.dirname(__file__), 'templates')
    STATIC_PATH = os.path.join(os.path.dirname(__file__), 'static')

    SECRET_KEY = 'you will never guess apeso'
    SECURITY_PASSWORD_SALT = 'never_guess_it'
    # mail
    MAIL_SERVER = 'smtp.ym.163.com'
    MAIL_PORT = 465
    MAIL_USERNAME = 'ApeSo@finder.ren'
    MAIL_PASSWORD = '723520wei'
    MAIL_USE_SSL = True
    MAIL_DEFAULT_SENDER = 'ApeSo@finder.ren'
    MAIL_RECIPIENTS = ['819799762@qq.com', 'chiabingwei@163.com']


class DevelopmentConfig(config):

    DEBUG = True


config = {
    'dev': DevelopmentConfig
}
