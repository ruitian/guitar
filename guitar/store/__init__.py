# -*- coding: utf-8 -*-
from mongokit import Document
from guitar import settings
from guitar import exc

conn = None

if not settings.MONGODB_REPLICASET:
    from mongokit import MongoClient

    mongo_uri = 'mongodb://%s:%s/%s' % (settings.MONGODB_HOST,
                                        settings.MONGODB_PORT,
                                        settings.MONGODB_DB)

    if settings.MONGODB_USER:
        mongo_uri = 'mongodb://%s:%s@%s:%s/%s' % (settings.MONGODB_USER,
                                                  settings.MONGODB_PWD,
                                                  settings.MONGODB_HOST,
                                                  settings.MONGODB_PORT,
                                                  settings.MONGODB_DB)

    conn = MongoClient(
        mongo_uri,
        max_pool_size=settings.MONGODB_MAX_POOL_SIZE,
        connectTimeoutMS=settings.MONGODB_CONNECT_TIMEOUT_MS,
        SocketTimeoutMS=settings.MONGODB_SOCKET_TIMEOUT_MS,
        waitQueueTimeoutMS=settings.MONGODB_WAIT_QUEUE_TIMEOUT_MS,
        waitQueueMultiple=settings.MONGODB_WAIT_QUEUE_MULTIPLE)

else:
    from mongokit import MongoReplicaSetClient

    mongo_uri = 'mongodb://%s/%s' % (
        settings.MONGODB_HOST, settings.MONGODB_DB)
    if settings.MONGODB_USER:
        mongo_uri = 'mongodb://%s:%s@%s/%s' % (
            settings.MONGODB_USER,
            settings.MONGODB_PWD,
            settings.MONGODB_HOST,
            settings.MONGODB_DB)

    conn = MongoReplicaSetClient(
        mongo_uri,
        max_pool_size=settings.MONGODB_MAX_POOL_SIZE,
        connectTimeoutMS=settings.MONGODB_CONNECT_TIMEOUT_MS,
        SocketTimeoutMS=settings.MONGODB_SOCKET_TIMEOUT_MS,
        waitQueueTimeoutMS=settings.MONGODB_WAIT_QUEUE_TIMEOUT_MS,
        waitQueueMultiple=settings.MONGODB_WAIT_QUEUE_MULTIPLE)


class BaseDoc(Document):
    __database__ = settings.MONGODB_DB

    use_schemaless = True

    def find_one_without_none(self, *args, **kwargs):
        rv = self.collection.find_one(wrap=self._obj_class, *args, **kwargs)
        if not rv:
            raise exc.InternetError(exc.Code.RESOURCE_NOT_FOUND,
                                    msg=self.collection.name,
                                    combine_messages=True)
        return rv


from .user import *  # noqa
