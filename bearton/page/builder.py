import json
import os
import sys
import warnings

import muspyche

from .. import util
from .. import config
from .. import db
from .. import schemes


def gathercontexts(pagepath, msgr, what='base'):
    pagemeta = json.loads(util.readfile(os.path.join(pagepath, 'meta.json')))
    msgr.debug('directly required contexts: {0}'.format(pagemeta['requires'][what]))
    gathered = pagemeta['requires'][what][:]
    for c in gathered:
        meta = schemes.inspector.getMeta(pagemeta['scheme'], c)
        gathered.extend([el for el in meta['requires'][what] if el not in gathered])
    msgr.debug('resolved required contexts: {0}'.format(gathered))
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
    path = os.path.abspath(path)
    dbpath = os.path.join(path, '.bearton', 'db', 'pages')
    pagepath = os.path.join(dbpath, page)
    msgr.debug('schemes: {0}'.format(schemes))
    msgr.debug('path: {0}'.format(path))
    msgr.debug('pagepath: {0}'.format(pagepath))
    meta = json.loads(util.readfile(os.path.join(pagepath, 'meta.json')))
    context = json.loads(util.readfile(os.path.join(pagepath, 'context.json')))
    context = loadcontexts(schemes, meta['scheme'], context, gathercontexts(pagepath, msgr, 'contexts'), msgr)
    context = loadbasecontexts(path, schemes, meta['scheme'], context, gathercontexts(pagepath, msgr, 'base'), msgr)
    template = os.path.join(schemes, meta['scheme'], 'elements', meta['name'], 'template.mustache')
    msgr.debug('reading template: {0}'.format(template))
    template = util.readfile(template)
    return muspyche.make(template, context, lookup=[os.path.join(schemes, meta['scheme'], 'elements')])

def build(path, schemes, page, msgr):
    meta = json.loads(util.readfile(os.path.join(path, '.bearton', 'db', 'pages', page, 'meta.json')))
    output = os.path.join(path, util.expandoutput(meta['output']))
    msgr.debug('written file to: {0}'.format(output))
    util.writefile(output, render(path, schemes, page, msgr))
