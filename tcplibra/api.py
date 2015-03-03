from handlers import *

from tornado.web import Application

class API(Application):
    def __init__(self, server, controller):
        super(API, self).__init__([
            (r"/", RootHandler),
            (r"/api/reals/?$", RealsHandler),
            (r"/api/reals/(?P<id>\d+)/?$", RealHandler),
        ])

        self.server = server
        self.controller = controller
