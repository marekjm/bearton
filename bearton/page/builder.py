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

def loadcontexts(schemes, scheme, context, required, msgr):
    for element in required:
        cntxt = json.loads(util.readfile(os.path.join(schemes, scheme, 'elements', element, 'context.json')))
        for k, v in cntxt.items():
            if k in context: msgr.message('warning: key conflict in context: {0}: {1} -> {2}'.format(k, context[k], v))
            context[k] = v
    return context

def loadbasecontexts(path, schemes, scheme, context, required, msgr):
    for element in required:
        conpath = os.path.join(path, '.bearton', 'db', 'base', element, 'context.json')
        if not os.path.isfile(conpath):
            msgr.debug('warning: loading default context for base element: {0}'.format(element))
            conpath = os.path.join(schemes, scheme, 'elements', element, 'context.json')
        cntxt = json.loads(util.readfile(conpath))
        for k, v in cntxt.items():
            if k in context: msgr.message('warning: key conflict in context: {0}: {1} -> {2}'.format(k, context[k], v))
            context[k] = v
    return context

def render(path, schemes, page, msgr):
    dbpath = os.path.join(path, '.bearton', 'db', 'pages')
    pagepath = os.path.join(dbpath, page)
    msgr.debug('schemes: {0}'.format(schemes))
    msgr.debug('path: {0}'.format(path))
    msgr.debug('pagepath: {0}'.format(pagepath))
    meta = json.loads(util.readfile(os.path.join(pagepath, 'meta.json')))
    context = json.loads(util.readfile(os.path.join(pagepath, 'context.json')))
    gathered = gathercontexts(schemes, meta['scheme'], meta['requires']['contexts'], msgr)
    gathered_base = gathercontexts(schemes, meta['scheme'], meta['requires']['base'], msgr)
    context = loadcontexts(schemes, meta['scheme'], context, gathered, msgr)
    context = loadbasecontexts(path, schemes, meta['scheme'], context, gathered_base, msgr)
    msgr.debug('reading template')
    template = util.readfile(os.path.join(schemes, meta['scheme'], 'elements', meta['name'], 'template.mustache'))
    return muspyche.make(template, context, lookup=[os.path.join(schemes, meta['scheme'], 'elements')])

def build(path, schemes, page, msgr):
    output = os.path.join(path, util.expandoutput(meta['output']))
    msgr.debug('written file to: {0}'.format(output))
    util.writefile(output, render(path, schemes, scheme, msgr))
