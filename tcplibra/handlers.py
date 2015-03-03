
__all__ = ('RootHandler', 'RealsHandler', 'RealHandler')

import json

from tornado.web import RequestHandler

class RootHandler(RequestHandler):
    def get(self):
        self.redirect("/api/reals")

class RealsHandler(RequestHandler):
    def get(self):
        self.set_header('Content-Type', 'application/json')
        reals = self.application.controller.list()
        self.write(json.dumps([r.to_json() for r in reals]))

    def post(self):
        try:
            data = json.loads(self.request.body)
            real = self.application.controller.create(data)
        except ValueError, e:
            self.set_header('Content-Type', 'application/json')
            self.set_status(412)
            self.write(json.dumps({"error": e.message}))
        else:
            self.set_header('Content-Type', 'application/json')
            self.write(real.to_json())

class RealHandler(RequestHandler):
    def get(self, id):
        self.set_header('Content-Type', 'application/json')
        real = self.application.controller.get(int(1))

        if real:
            self.write(real.to_json())
        else:
            self.set_status(404)
            self.write('{"error": "real %s not found"}' % id)

    def delete(self, id):
        if self.application.controller.delete(int(1)):
            self.set_status(204)
            self.write('')
        else:
            self.set_status(404)
            self.write('{"error": "real %s not found"}' % id)
