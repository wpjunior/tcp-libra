import socket
from tornado.iostream import IOStream
from tornado import gen

class Session(object):
    def __init__(self, stream, address, server, real):
        print 'New session: %s:%d -> %s:%d' % (
            address[0], address[1], real.host, real.port
        )
        self.stream = stream
        self.address = address
        self.server = server
        self.real = real
        self.closing = False
        self.configure_connections()

    @gen.coroutine
    def configure_connections(self):
        self.stream.set_close_callback(self.on_disconnect)
        self.stream.read_until_close(
            callback=self.on_stream_finish,
            streaming_callback=self.on_streaming_callback)

        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0)

        self.out_stream = IOStream(s)

        try:
            yield self.out_stream.connect((self.real.host, self.real.port))
        except socket.error, e:
            self.real.available = False
            self.disconnect()

        self.out_stream.set_close_callback(self.on_out_disconnect)
        self.out_stream.read_until_close(
            callback=self.on_out_stream_finish,
            streaming_callback=self.on_out_streaming_callback)

    def disconnect(self):
        if not self.closing:
            self.closing = True
            self.stream.close()
            self.out_stream.close()
            self.real.connections = self.real.connections - 1

    def on_disconnect(self):
        self.disconnect()

    def on_streaming_callback(self, data):
        if data:
            self.out_stream.write(data)

    def on_stream_finish(self, data):
        if data:
            self.out_stream.write(data)

        self.out_stream.close()

    def on_out_disconnect(self):
        self.disconnect()

    def on_out_streaming_callback(self, data):
        if data:
            self.stream.write(data)

    def on_out_stream_finish(self, data):
        if data:
            self.stream.write(data)

        self.stream.close()
