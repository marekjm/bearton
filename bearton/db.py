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

    def _updatemeta(self, schemes):
        new_meta = json.loads(util.readfile(os.path.join(schemes, self._meta['scheme'], 'elements', self._meta['name'], 'meta.json')))
        scheme, name = self._meta['scheme'], self._meta['name']
        final = util.dictmerge(self._meta, new_meta)
        for k, v in [('scheme', scheme), ('name', name)]:
            if k not in final: final[k] = v
        code = 0
        if final != self._meta:
            self._meta = final
            code = 1
            self._changed = True
        return code

    def _updatecontext(self, schemes):
        new = json.loads(util.readfile(os.path.join(schemes, self._meta['scheme'], 'elements', self._meta['name'], 'context.json')))
        code = 0
        final = util.dictmerge(base=self._context, update=new, overwrites=False)
        code = 0
        if final != self._context:
            self._context = final
            code = 2
            self._changed = True
        return code

    def update(self, schemes):
        """Return codes:

        0 - nothing was updated,
        1 - metadata was updated,
        2 - context was updated,
        3 - metadata and context were updated,
        """
        code = 0
        code += self._updatemeta(schemes)
        code += self._updatecontext(schemes)
        return code

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
        """Updates entries in database.
        Return value is a tuple: (metadata, contexts) where

        * `metadata` is a list of entries whose metadata was updated,
        * `contexts` is a list of entries whose context was updated,
        """
        if not schemes: schemes = os.path.join(self._rawpath, 'schemes')
        metadata, contexts = [], []
        for entry in self:
            ret_code = entry.update(schemes)
            if ret_code == 0: pass
            if ret_code in [1, 3] and entry._entry not in metadata: metadata.append(entry._entry)
            if ret_code in [2, 3] and entry._entry not in contexts: contexts.append(entry._entry)
        return (metadata, contexts)
