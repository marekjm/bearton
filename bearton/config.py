import json
import os

from . import util
from .errors import *

DEFAULT = {'scheme': 'default'}

class Configuration:
    """Class implementing interface to Bearton site configuration.
    """
    def __init__(self, path='.'):
        self._path = (path if path.endswith('config.json') else os.path.join(path, 'config.json'))
        self._conf = None

    def __contains__(self, key):
        return key in self._conf

    def __getitem__(self, key):
        return self._conf[key]

    def __setitem__(self, key, value):
        self._conf[key] = value

    def __iter__(self):
        return iter(self._conf)

    def load(self):
        """Loads configuration file.
        """
        conf = json.loads(util.io.read(self._path, default=json.dumps(DEFAULT)))
        if conf is not None: self._conf = conf
        else: self.default()
        return self

    def unload(self):
        """Unloads configuration from the instance.
        """
        self._conf = None

    def default(self):
        """Return configuration to default state.
        """
        self._conf = {}
        for k, v in DEFAULT.items(): self._conf[k] = v
        return self

    def store(self):
        """Stores configration file and
        writes any changes made.
        """
        if self._conf is not None and self._path is not None: util.io.write(path=self._path, s=json.dumps(self._conf))
        return self

    def get(self, key, default=None):
        """Return value of `key` if `key` is present, raise `KeyError` otherwise.
        If default is provided, and key is not found this value is returned instead of
        exception being raised.
        """
        if key not in self and default is None: raise KeyError(key)
        return (self[key] if key in self else default)

    def set(self, key, value):
        self[key] = value
        return self

    def remove(self, key):
        del self._conf[key]
        return self

    def pop(self, key):
        value = self.get(key)
        self.remove(key)
        return value

    def items(self):
        return [(k, v) for k, v in self._conf.items()]

    def keys(self):
        return [key for key in self]
