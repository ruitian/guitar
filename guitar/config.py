# -*- coding: utf-8 -*-
import os  # noqa
import uuid
import base64

DEBUG = True

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

COOKIE_SECRET = base64.b64encode(uuid.uuid4().bytes + uuid.uuid4().bytes)
TEMPLATE_PATH = os.path.join(os.path.dirname(__file__), 'templates')
STATIC_PATH = os.path.join(os.path.dirname(__file__), 'static')
