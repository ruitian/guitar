# -*- coding: utf-8 -*-
import json
import bson
import datetime
import time


def _handler_object_for_json(obj):
    if isinstance(obj, bson.ObjectId):
        return oid2str(obj)
    if isinstance(obj, datetime.datetime):
        return datetime2timestamp(obj) * 1000
    if hasattr(obj, 'to_dict'):
        return obj.to_dict()


def decode_json(json_str):
    return json.loads(json_str)


def encode_json(data):
    return json.dumps(data,
                      default=_handler_object_for_json, ensure_ascii=False)


def oid2str(data, b64=True):
    if isinstance(data, bson.ObjectId):
        return str(data)
    return data


def datetime2timestamp(dtime):
    if isinstance(dtime, datetime.datetime):
        return long(time.mktime(dtime.timetuple()))
    return dtime
