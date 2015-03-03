
from tornado.ioloop import IOLoop

from tornado.tcpserver import TCPServer
from tornado.tcpclient import TCPClient

from controller import Controller
from session import Session
from api import API

class Server(TCPServer):
    mark_reavailable_real_timeout = 30 # seconds

    def __init__(self, controller):
        super(Server, self).__init__()

        self.controller = controller
        self.controller.on_create(self._on_real_created)
        self.controller.on_delete(self._on_real_deleted)

        self.reals_sorted = self.controller.list()
        self.balance_reals()

    def _on_real_created(self, real):
        self.reals_sorted.append(real)
        real.on_changed(self.on_real_changed)
        self.balance_reals()

    def _on_real_deleted(self, real):
        self.reals_sorted.remove(real)
        self.balance_reals()

    def handle_stream(self, stream, address):
        real = self.get_available_real()

        # no available real
        if not real:
            stream.close()
            return

        Session(stream, address, server=self, real=real)

    def get_available_real(self):
        for real in self.reals_sorted:
            if not real.available:
                continue

            real.connections = real.connections + 1

            self.balance_reals()

            return real

    def balance_reals(self):
        self.reals_sorted.sort()

    def on_real_changed(self, real):
        self.balance_reals()

        if not real.available:
            IOLoop.instance().call_later(
                self.mark_reavailable_real_timeout,
                self.mark_real_available, real)

    def mark_real_available(self, real):
        real.available = True

def run():
    controller = Controller()

    server = Server(controller)
    server.listen(4000)

    print 'Server running at port 4000'

    api = API(server, controller)
    api.listen(4001)
    print 'API running at port 4001'

    IOLoop.instance().start()

if __name__ == '__main__':
    run()
