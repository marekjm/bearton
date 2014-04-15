import json
import os
import sys
import warnings

import muspyche

from .. import util
from .. import config


def getcontext(schemepath, element):
    elpath = os.path.join(schemepath, 'elements', element)
    cntxt = util.readfile(os.path.join(elpath, 'context.json'))
    try:
        context, error = json.loads(cntxt), None
    except Exception as e:
        context, error = {}, e
    finally:
        pass
    if error is not None:
        raise type(e)('while loading context for: {0}: {1}'.format(os.path.abspath(elpath), e))
    return context

def getmeta(schemepath, element):
    elpath = os.path.join(schemepath, 'elements', element)
    meta = util.readfile(os.path.join(elpath, 'meta.json'))
    try:
        meta, error = json.loads(meta), None
    except Exception as e:
        meta, error = {}, e
    finally:
        pass
    if error is not None:
        raise type(e)('while loading metadata for: {0}: {1}'.format(os.path.abspath(elpath), e))
    return meta


class Element:
    """Class used to build objects.
    """
    def __init__(self, scheme, element):
        self._scheme = scheme
        self._element = element
        self._template, self._context = '', {}
        self._meta = {}

    def _loadtemplate(self, schemepath):
        elpath = os.path.join(schemepath, 'elements', self._element)
        tmplt = util.readfile(os.path.join(elpath, 'template.mustache'))
        try:
            self._template = muspyche.parser.parse(tmplt, lookup=[elpath, os.path.join(schemepath, 'elements')])
        except Exception as e:
            raise type(e)('while loading template for: {0}: {1}'.format(os.path.abspath(elpath), e))

    def _loadmeta(self, schemepath):
        self._meta = getmeta(schemepath, self._element)

    def _gathercontexts(self, schemepath):
        contexts = self._meta['requires']['contexts'][:]
        for element in self._meta['requires']['contexts']:
            meta = getmeta(schemepath, element)
            contexts.extend([req for req in meta['requires']['contexts'] if req not in contexts])
        return contexts

    def _loadcontext(self, schemepath):
        required = self._gathercontexts(schemepath)
        required.insert(0, self._element)
        for element in required:
            cntxt = getcontext(schemepath, element)
            for k, v in cntxt.items():
                if k in self._context:
                    warnings.warn('bearton: warning: conflicting key in required contexts: {0}: {1} -> {2}'.format(k, self._context[k], v))
                self._context[k] = v

    def load(self):
        """Loads element's metadata, context(s) and template.
        """
        schemepath = os.path.join('schemes', conf.Configuration().load().get('scheme'))
        self._loadmeta(schemepath)
        self._loadcontext(schemepath)
        self._loadtemplate(schemepath)
        return self


def build(path, page, msgr):
    msgr.debug('path: {0}'.format(path))
    dbpath = os.path.join(path, '.bearton', 'db')
    msgr.debug('dbpath: {0}'.format(dbpath))
    msgr.debug('page: {0}'.format(page))
