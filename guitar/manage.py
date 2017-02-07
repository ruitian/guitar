# -*- coding: utf-8 -*-
from tornado.ioloop import IOLoop
from tornado.web import Application
from tornado.httpclient import AsyncHTTPClient
from tornado.options import options, define, parse_command_line
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

from guitar.handlers import route
from guitar import config  # noqa

define(
    'port', default=8080, help='run on the ginven port', type=int)
define(
    'debug', default=True, help='run in debug mode with authreload', type=bool)
define(
    'db_connection_str', default='mysql://root@localhost/test',
    help='Database connection string for application')

db_engine = create_engine(options.db_connection_str)
db_session = sessionmaker()

AsyncHTTPClient.configure('tornado.simple_httpclient\
.SimpleAsyncHTTPClient', max_clients=3)


class MyApplication(Application):
    def __init__(self, *args, **kwargs):
        routes = route.get_routes()
        settings = {
            'debug': config.DEBUG,
            'cookie_secret': config.COOKIE_SECRET,
            'static_path': config.STATIC_PATH,
            'template_path': config.TEMPLATE_PATH,
            'db_session': db_session
        }
        self.session = kwargs.pop('session')
        self.session.configure(bind=db_engine)
        Application.__init__(self, routes, **settings)


def main():
    application = MyApplication(session=db_session)
    parse_command_line()
    application.listen(options.port, '0.0.0.0', xheaders=False)
    IOLoop.current().start()


if __name__ == '__main__':
    main()
