
class Real(object):
    change_listenners = []

    def __init__(self, id, host, port):
        self.id = id
        self.host = host
        self.port = port
        self._available = True
        self._connections = 0

    def to_json(self):
        return {
            'id': self.id,
            'host': self.host,
            'port': self.port,
            'available': self._available,
            'connections': self._connections
        }

    def store_format(self):
        return {
            'id': self.id,
            'host': self.host,
            'port': self.port
        }

    def on_changed(self, callback):
        self.change_listenners.append(callback)

    def _on_changed(self):
        for item in self.change_listenners:
            item(self)

    @property
    def available(self):
        return self._available

    @available.setter
    def available(self, value):
        self._available = value
        self._on_changed()

    @property
    def connections(self):
        return self._connections

    def __repr__(self):
        return repr(self.to_json())

    @connections.setter
    def connections(self, value):
        self._connections = value
        self._on_changed()

    def __cmp__(self, other):
        if self._available == other._available:
            if self._connections < other._connections:
                return -1
            elif self._connections > other._connections:
                return 1
            else:
                return 0

        elif self._available:
            return -1
        else:
            return 1
