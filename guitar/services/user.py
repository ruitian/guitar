# -*- coding: utf-8 -*-
from werkzeug import generate_password_hash, check_password_hash
from guitar.store import conn


def get_user_id():

    user = conn.Counters.find_and_modify(
        {'name': 'user_id'},
        {'$inc': {'user_id': 1}}
    )
    return user['user_id']


def user_register(arguments):

    user = list(conn.User.find({'username': arguments['username']}))
    if len(user) == 0:
        arguments.update({
            'user_id': get_user_id(),
            'password': generate_password_hash(arguments['password'])
        })
        user = conn.User()
        user.update(arguments)
        user.save()
    else:
        return user


def check_password(arguments):

    users = list(conn.User.find({'username': arguments['username']}))
    if len(users) != 0:
        for user in users:
            return check_password_hash(user['password'], arguments['password'])
    return False
