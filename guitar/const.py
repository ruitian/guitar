# -*- coding: utf-8 -*-

def enum(*sequential, **named):
    enums = dict(zip(sequential, range(len(sequential))), **named)
    return type('enum', (), enums)

from mongokit import INDEX_ASCENDING, INDEX_DESCENDING

MONGO_INDEX = enum(
    ASCENDING=INDEX_ASCENDING,
    DESCENDING=INDEX_DESCENDING
)
