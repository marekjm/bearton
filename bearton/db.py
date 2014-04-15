"""File implementing easier access to Bearton databases.
"""

import json
import os
import shutil

from . import util


class Entry:
    """Single entry in the database.
    """
    def __init__(self, path, entry):
        self._path = path
        self._entry = entry
        self._meta = {}
        self._context = {}
        self._changed = False

    def load(self):
        epath = os.path.join(self._path, self._entry)
        self._meta = json.loads(util.readfile(os.path.join(epath, 'meta.json')))
        self._context = json.loads(util.readfile(os.path.join(epath, 'context.json')))
        return self

    def setinmeta(self, key, value=''):
        self._meta[key] = value
        self._changed = True

    def store(self):
        epath = os.path.join(self._path, self._entry)
        if self._changed:
            util.writefile(os.path.join(epath, 'meta.json'), json.dumps(self._meta))
            util.writefile(os.path.join(epath, 'context.json'), json.dumps(self._context))
        self._changed = False

    def remove(self):
        shutil.rmtree(os.path.join(self._path, self._entry))


class Database:
    """Object providing database interface.
    """
    def __init__(self, path):
        self._path = os.path.join(path, '.bearton', 'db', 'pages')
        self._db = None

    def __iter__(self):
        return iter([self._db[key] for key in self._db])

    def _readdb(self):
        entries = os.listdir(self._path)
        entries = [(entry, Entry(self._path, entry).load()) for entry in entries]
        return dict(entries)

    def load(self):
        self._db = self._readdb()
        return self

    def store(self):
        for entry in self: entry.store()
        return self

    def unload(self):
        self._db = None

    def keys(self):
        return [key for key in self._db]

    def query(self, scheme, element, queryd={}):
        subdb = {}
        for key, entry in self._db.items():
            if scheme == entry['scheme'] and element == entry['name']: subdb[key] = entry
        pool = []
        for key, entry in subdb.items():
            match = (True if queryd != {} else False)
            for k, v in queryd.items():
                if k not in entry._meta:
                    match = False
                    break
                if entry._meta[k] != queryd[k]:
                    match = False
                    break
            if match: pool.append( (key, entry) )
        return pool

    def wipe(self):
        for entry in self: entry.remove()
        self._readdb()
