import json
import os

from . import util
from .exceptions import *


class Configuration:
    """Class implementing interface to Bearton site configuration.
    """
    # class variable, so when one copy of configuratin is loaded as guarded all become
    # the instance that set config to guarded stance becomes a guard and only it can unguard the config (by calling .unload())
    _guarded, _guard = False, None

    def __init__(self, path='.'):
        self._path = path
        self._conf = {}

    def __contains__(self, key):
        return key in self._conf

    def __getitem__(self, key):
        return self._conf[key]

    def __setitem__(self, key, value):
        self._conf[key] = value

    def __iter__(self):
        return iter(self._conf)

    def _getpath(self):
        """Tries to find a path to config JSON file.
        """
        base, path = os.path.abspath(self._path), ''
        while True and os.path.split(base)[1] != '':
            path = os.path.join(base, '.bearton', 'config.json')
            if os.path.isfile(path): break
            base, path = os.path.split(base)[0], ''
        if not path:
            raise BeartonError('cannot find Bearton configuration file: start directory: {0}'.format(os.path.abspath(self._path)))
        else:
            return path

    def load(self, guard=False):
        """Loads configuration file.
        If `guard` is true, it will guard the file from being written; the runtime copy may be modified at will however.
        """
        if Configuration._guarded is not True:
            Configuration._guarded = guard
            Configuration._guard = self
        self._path = self._getpath()
        conf = json.loads(util.readfile(self._path))
        if conf is not None: self._conf = conf
        else: self.default()
        return self

    def unload(self):
        """Unloads configuration from the instance.
        """
        if Configuration._guard == self and Configuration._guarded is True: Configuration._guarded = False
        self._conf = None

    def default(self):
        """Return configuration to default state.
        """
        self._conf = {'scheme': 'default'}
        return self

    def store(self):
        """Stores configration file and
        writes any changes made.
        """
        if Configuration._guarded is not True: util.writefile(path=self._path, s=json.dumps(self._conf))
        return self

    def get(self, key):
        return self[key]

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

    def kvalues(self):
        return [(k, v) for k, v in self._conf.items()]

    def keys(self):
        return [key for key in self]
