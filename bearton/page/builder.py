import json
import os
import sys
import warnings

import muspyche

from .. import util
from .. import config
from .. import db


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
    msgr.debug('reading template')
    template = util.readfile(os.path.join(schemes, meta['scheme'], 'elements', meta['name'], 'template.mustache'))
    rendered = ''
    rendered = muspyche.make(template, context, lookup=[os.path.join(schemes, meta['scheme'], 'elements')])
    msgr.message('\n')
    msgr.message(rendered, 0)
