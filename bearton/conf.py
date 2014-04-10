import json
import os

from . import util
from .exceptions import *


class Configuration:
    """Class implementing interface to Bearton site configuration.
    """
    def __init__(self, path=''):
        self._path = path
        self._conf = {}

    def __str__(self):
        return str(self._conf)

    def __contains__(self, key):
        return key in self._conf

    def __getitem__(self, key):
        return self._conf[key]

    def __setitem__(self, key, value):
        self._conf[key] = value

    def __iter__(self):
        return iter(self._conf)

    def _getpath(self):
        """Tries to find a path to conf dictionary.
        """
        base, path = os.path.abspath('./site'), ''
        while True and os.path.split(base)[1] != '':
            path = os.path.join(base, 'conf.json')
            if os.path.isfile(path): break
            base, path = os.path.split(base)[0], ''
        if not path:
            raise BeartonError('cannot find Bearton configuration file: start directory: {0}'.format(os.path.abspath('./site')))
        else:
            return path

    def load(self):
        """Loads configuration file.
        """
        self._path = self._getpath()
        self._conf = json.loads(util.readfile(self._path))
        return self

    def store(self):
        """Stores configration file and
        writes any changes made.
        """
        util.writefile(path=self._path, s=json.dumps(self._conf))
        return self

    def get(self, key):
        return self[key]

    def set(self, key, value):
        self[key] = value
        return self

    def remove(self, key):
        del self._conf[key]
        return self
