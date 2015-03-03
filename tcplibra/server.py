
from tornado.ioloop import IOLoop

from tornado.tcpserver import TCPServer
from tornado.tcpclient import TCPClient

from controller import Controller
from session import Session
from api import API

class Server(TCPServer):
    def __init__(self, controller, reavailable_after=30):
        super(Server, self).__init__()

        self.controller = controller
        self.reavailable_after = reavailable_after

        self.controller.on_create(self._on_real_created)
        self.controller.on_delete(self._on_real_deleted)

        self.reals_sorted = self.controller.list()

        for real in self.reals_sorted:
            real.on_changed(self.on_real_changed)

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
                self.reavailable_after,
                self.mark_real_available, real)

    def mark_real_available(self, real):
        real.available = True

def run():
    import argparse

    parser = argparse.ArgumentParser(
        description='The simple tcp load balancer written in tornado')

    parser.add_argument('-p', '--port',
                        default='4000',
                        type=int,
                        help='server port, default (default: 4000)')

    parser.add_argument('-a', '--api-port',
                        default='4001',
                        type=int,
                        help='api port, default (default: 4001)')

    parser.add_argument('-r', '--reavailable-after',
                        default='30',
                        type=int,
                        help='reavailable real after x seconds, default (default: 30)')

    args = parser.parse_args()

    controller = Controller()

    server = Server(controller, reavailable_after=args.reavailable_after)
    server.listen(args.port)

    print 'Server running at port %d' % args.port

    api = API(server, controller)
    api.listen(args.api_port)
    print 'API running at port %d' % args.api_port

    IOLoop.instance().start()

if __name__ == '__main__':
    run()
