# -*- coding: utf-8 -*-
from mongokit import INDEX_ASCENDING, INDEX_DESCENDING


def enum(*sequential, **named):
    enums = dict(zip(sequential, range(len(sequential))), **named)
    return type('enum', (), enums)


MONGO_INDEX = enum(
    ASCENDING=INDEX_ASCENDING,
    DESCENDING=INDEX_DESCENDING
)
