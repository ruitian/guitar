# -*- coding: utf-8 -*-
from . import conn, BaseDoc
from guitar.const import MONGO_INDEX

import datetime

@conn.register
class User(BaseDoc):
    __collection__ = 'user'

    structure = {
        'user_id': int,
        'username': basestring,
        'password': basestring,

        'ctime': datetime.datetime,
        'utime': datetime.datetime
    }

    require_fields = {'user_id', 'username', 'password'}
    default_values = {
        'ctime': datetime.datetime.utcnow,
        'utime': datetime.datetime.utcnow
    }
    indexes = [
        {
            'fields': [('username', MONGO_INDEX.ASCENDING),
                       ('user_id', MONGO_INDEX.ASCENDING)],
            'nuique': True
        }
    ]


@conn.register
class Counters(BaseDoc):
    __collection__ = 'counters'

    structure = {
        'name': basestring,
        'user_id': int,
    }

    default_values = {
        'user_id': 0
    }
