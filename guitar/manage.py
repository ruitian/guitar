# -*- coding: utf-8 -*-
import session

from tornado.ioloop import IOLoop
from tornado.web import Application
from tornado.httpclient import AsyncHTTPClient
from tornado.options import options, define, parse_command_line
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from raven.contrib.tornado import AsyncSentryClient
from redis import Redis

from guitar.handlers import route
from guitar.config import config as conf
from guitar.models import Base

define(
    'port', default=8080, help='run on the ginven port', type=int)
define(
    'debug', default=True, help='run in debug mode with authreload', type=bool)
define(
    'db_connection_str', default='mysql://root@localhost/apeso',
    help='Database connection string for application')

db_engine = create_engine(options.db_connection_str)
db_session = sessionmaker(autoflush=False)
AsyncHTTPClient.configure('tornado.simple_httpclient\
.SimpleAsyncHTTPClient', max_clients=3)


class MyApplication(Application):
    def __init__(self, *args, **kwargs):
        routes = route.get_routes()
        config = conf.get('dev')
        settings = dict(
            debug=config.DEBUG,
            secret_key=config.SECRET_KEY,
            session_secret=config.SECRET_KEY,
            session_timeout=config.SESSION_TIMEOUT,
            store_options=config.REDIS_STORE,
            password_salt=config.SECURITY_PASSWORD_SALT,
            cookie_secret=config.SECRET_KEY,
            static_path=config.STATIC_PATH,
            template_path=config.TEMPLATE_PATH,
            code_temp=config.CODE_TEMP,
            db_session=db_session,
            mail_server=config.MAIL_SERVER,
            mail_port=config.MAIL_PORT,
            mail_username=config.MAIL_USERNAME,
            mail_password=config.MAIL_PASSWORD,
            mail_use_ssl=config.MAIL_USE_SSL,
            mail_default_sender=config.MAIL_DEFAULT_SENDER,
            login_url='/api/account/login'
        )
        self.session = kwargs.pop('session')
        self.session.configure(bind=db_engine)
        self.db_redis = Redis(
            host=settings['store_options']['redis_host'],
            password=settings['store_options']['redis_pass'],
            port=settings['store_options']['redis_port'],
            db=settings['store_options']['redis_db']
        )
        Application.__init__(self, routes, **settings)
        self.session_manager = session.SessionManager(
            settings["session_secret"],
            settings["store_options"],
            settings["session_timeout"])
        # sentry
        self.sentry_client = AsyncSentryClient(
            'http://ac79d38965af43bf8b283ea80cedad0c:3aeb9e2bdecf4955bc92e1d3b1e3ee0e@127.0.0.1:9000/2'
        )


def create_db():
    Base.metadata.create_all(db_engine)


def main():
    application = MyApplication(session=db_session)
    parse_command_line()
    application.listen(options.port, '0.0.0.0', xheaders=False)
    IOLoop.current().start()


if __name__ == '__main__':
    main()
