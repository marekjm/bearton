"""File implementing easier access to Bearton databases.
"""

import json
import os
import re
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
        meta = {'requires': {'contexts': [], 'base': []},
                'output': '',
                'singular': True,
                'base': False,
                }
        loaded = json.loads(util.readfile(os.path.join(epath, 'meta.json')))
        self._meta = util.dictmerge(meta, loaded, removals=False)
        self._context = json.loads(util.readfile(os.path.join(epath, 'context.json')))
        return self

    def _updatemeta(self, schemes):
        new_meta = json.loads(util.readfile(os.path.join(schemes, self._meta['scheme'], 'elements', self._meta['name'], 'meta.json')))
        scheme, name = self._meta['scheme'], self._meta['name']
        output = (self._meta['output'] if not self._meta['singular'] else new_meta['output'])
        final = util.dictmerge(self._meta, new_meta)
        for k, v in [('scheme', scheme), ('name', name)]:
            if k not in final: final[k] = v
        final['output'] = output
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

    def metag(self, key):
        return self._meta[key]

    def getsignature(self, s):
        """Provides convinient way to get database entry's signature.
        Signature is a string containing field-identifiers - special substrings which return values from entry's meta or
        context.

        TODO: only access to top-level keys is provided.

        Identifiers can have a form of:

        {:key@}                 - returns key (hash id) of the entry, "key" is hardcoded,
        {:foo@meta}             - returns value of 'foo' from entry's meta,
        {:foo@context}, {:foo}  - returns value of 'foo' from entry's context,

        Keys that are not found in meta or context return empty strings.
        """
        regex_key = re.compile('{:([a-z0-9-_]+)(@[a-z0-9-_]*)?}')
        keys = regex_key.findall(s)
        for key, where in keys:
            identifier = '{:' + '{0}{1}'.format(key, where) + '}'
            if where == '@' and key == 'key':
                value = self._entry
            elif where in ['@meta', '']:
                value = (self._meta[key] if key in self._meta else '')
            elif where == '@context':
                value = (self._context[key] if key in self._context else '')
            else:
                raise KeyError('invalid identifier: {0}'.format(identifier))
            s = s.replace(identifier, value)
        return s

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

    def query(self, scheme, element, queryd={}, querytags=[]):
        """Queries database.
        First, it matches scheme and elemeent.
        If scheme is empty or element is empty, only one will be used to match.
        If both scheme and element are empty, nothing will be matched.

        After initial scheme/element matching, queryd-matching is performed
        against sub-pool of previously matched entries.
        It is key-to-key matching - if key is present in queryd but not in given entry,
        entry is not matched.

        Queryd matching logic:

        - if key is present in neither meta nor context, entry is not matched;
        - if key is present in queryd and in meta, increase match by one;
            - if values of the key are equal, increase match by one;
        - if key is present queryd and in context, increase match by one;
            - if values of the key are equal, increase match by one;
        - if key is present in BOTH meta and context (is an ambigious one), divide match by two;
        - for every tag present both in querytags and entry tags, increase match by one;
        - for every tag that is required to be matched and is not present in tags, decrease match by one, else increase by one;
        - for every tag that is required to be NOT matched and is present in tags, decrease match by one, else increase by one;
        """
        subdb = {}
        for key, entry in self._db.items():
            if not scheme and not element: continue
            if (scheme == entry._meta['scheme'] if scheme else True) and (element == entry._meta['name'] if element else True): subdb[key] = entry
        pool = []
        for key, entry in subdb.items():
            match = 0   # TODO: match should be an indicator of how well the entry matches the query
            if not len(queryd.keys()): match = 2
            for k, v in queryd.items():
                if k in entry._meta:
                    match += 1
                    if entry._meta[k] == queryd[k]: match += 1
            if match > 0: pool.append( (key, entry) )
        return pool

    def get(self, key):
        return self._db[key]

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
