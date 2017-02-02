# -*- coding: utf-8 -*-
from tornado.ioloop import IOLoop
from tornado.web import Application
from tornado.httpclient import AsyncHTTPClient
from tornado.options import options, define, parse_command_line
from guitar.handlers import route
from guitar import settings

define(
    'port', default=8080, help='run on the ginven port', type=int)
define(
    'debug', default=True, help='run in debug mode with authreload', type=bool)

AsyncHTTPClient.configure('tornado.simple_httpclient\
.SimpleAsyncHTTPClient', max_clients=3)

parse_command_line(final=True)

routes = route.get_routes()

application = Application(
    routes,
    debug=True)


def main():
    application.listen(options.port, '0.0.0.0', xheaders=False)
    IOLoop.current().start()

if __name__ == '__main__':
    main()
