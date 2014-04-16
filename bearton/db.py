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

    def update(self, schemes):
        new_meta = json.loads(util.readfile(os.path.join(schemes, self._meta['scheme'], 'elements', self._meta['name'], 'meta.json')))
        for key, value in new_meta.items():
            if key not in self._meta:
                self._meta[key] = value
                self._changed = True
            if self._meta[key] != value:
                self._meta[key] = value
                self._changed = True
        return self

    def setinmeta(self, key, value=''):
        self._meta[key] = value
        self._changed = True

    def store(self):
        epath = os.path.join(self._path, self._entry)
        if self._changed:
            print('stored:', self._path)
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
        self._rawpath = path
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
            if scheme == entry._meta['scheme'] and element == entry._meta['name']: subdb[key] = entry
        pool = []
        for key, entry in subdb.items():
            match = True
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

    def update(self, schemes=''):
        if not schemes: schemes = os.path.join(self._rawpath, 'schemes')
        for entry in self: entry.update(schemes)
