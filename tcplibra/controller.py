import json
import os

from models import Real

class Controller(object):
    max_id = 0
    index = {}
    _create_listeners = []
    _delete_listeners = []

    def __init__(self):
        self.reals_path = os.path.expanduser('~/.libra/reals.json')

        dirname = os.path.dirname(self.reals_path)
        if not os.path.exists(dirname):
            os.mkdir(dirname)

        self._read_file()

    def on_create(self, callback):
        self._create_listeners.append(callback)

    def on_delete(self, callback):
        self._delete_listeners.append(callback)

    def create(self, data):
        if not 'host' in data:
            raise ValueError('Required field `host`')

        if not 'port' in data:
            raise ValueError('Required field `port`')

        self.max_id += 1

        real = Real(self.max_id, data['host'], data['port'])
        self.index[self.max_id] = real

        self._on_created(real)
        self._store()

        return real

    def list(self):
        return self.index.values()

    def get(self, id):
        return self.index.get(id)

    def delete(self, id):
        if id in self.index:
            real = self.index[id]

            del self.index[id]

            self._on_delete(real)
            self._store()

            return True

        return False

    def _on_created(self, data):
        for item in self._create_listeners:
            item(data)

    def _on_delete(self, data):
        for item in self._delete_listeners:
            item(data)

    def _store(self):
        data = json.dumps([r.store_format() for r in self.index.values()],
                          indent=2)

        with open(self.reals_path, 'wb') as f:
            f.write(data)

    def _read_file(self):
        if not os.path.exists(self.reals_path):
            return

        with open(self.reals_path, 'rb') as f:
            items = json.loads(f.read())

            for item in items:
                real = Real(item['id'], item['host'], item['port'])
                self.index[real.id] = real

            if self.index:
                self.max_id = sum([r.id for r in self.index.values()])
