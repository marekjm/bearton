import json
import os
import sys
import warnings

import muspyche

from .. import util
from .. import config
from .. import db


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


def gathercontexts(schemes, scheme, contexts, msgr):
    msgr.debug('required contexts: {0}'.format(contexts))
    gathered = []
    while gathered != contexts:
        gathered = contexts[:]
        for i in contexts:
            meta = json.loads(util.readfile(os.path.join(schemes, scheme, 'elements', i, 'meta.json')))
            gathered.extend([con for con in meta['requires']['contexts'] if con not in gathered])
        contexts = gathered[:]
    msgr.debug('final required contexts: {0}'.format(contexts))
    return gathered

def loadcontexts(schemes, scheme, context, required):
    for element in required:
        cntxt = json.loads(util.readfile(os.path.join(schemes, scheme, 'elements', element, 'context.json')))
        for k, v in cntxt.items():
            if k in context: msgr.message('warning: key conflict in context: {0}: {1} -> {2}'.format(k, context[k], v))
            context[k] = v
    return context

def build(path, schemes, page, msgr):
    dbpath = os.path.join(path, '.bearton', 'db')
    pagepath = os.path.join(dbpath, page)
    msgr.debug('schemes: {0}'.format(schemes))
    msgr.debug('path: {0}'.format(path))
    msgr.debug('dbpath: {0}'.format(dbpath))
    msgr.debug('pagepath: {0}'.format(pagepath))
    meta = json.loads(util.readfile(os.path.join(pagepath, 'meta.json')))
    msgr.debug('meta: {0}'.format(meta))
    context = json.loads(util.readfile(os.path.join(pagepath, 'context.json')))
    gathered = gathercontexts(schemes, meta['scheme'], meta['requires']['contexts'], msgr)
    msgr.debug('context: {0}'.format(context))
    context = loadcontexts(schemes, meta['scheme'], context, gathered)
    msgr.debug('final context: {0}'.format(context))
