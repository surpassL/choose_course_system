import os
from conf import setting
import pickle


def load_db(kind, name):
    name = '%s.pkl' % name
    path = os.path.join(setting.DB_PATH, kind, name)
    if os.path.exists(path):
        with open(path, 'rb') as f:
            adj = pickle.load(f)
        return adj


class Base:
    def dump_db(self):
        name = '%s.pkl' % self.name
        path = os.path.join(setting.DB_PATH, self.kind, name)
        with open(path, 'wb') as f:
            pickle.dump(self, f)
