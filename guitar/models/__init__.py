# -*- coding: utf-8 -*-
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


from .user import UserModel  # noqa
from .user_info import UserinfoModel  # noqa
from .tag import TagModel  # noqa
from .relations import *  # noqa
