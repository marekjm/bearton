import json
import os
import sys
import warnings

import muspyche

try:
    import markdown2 as markdown
except ImportError:
    try:
        import markdown # try different library
    except ImportError:
        markdown = None  # no Markdown support
    finally:
        pass
finally:
    pass

from .. import util
from .. import config
from .. import db
from .. import schemes


def gathercontexts(path, pagepath, msgr, what='base'):
    pagemeta = json.loads(util.readfile(os.path.join(pagepath, 'meta.json')))
    msgr.debug('directly required contexts ({1}): {0}'.format(pagemeta['requires'][what], what))
    gathered = pagemeta['requires'][what][:]
    for c in gathered:
        if c[0] == '#':
            required = [c]
        else:
            required = schemes.inspector.getMeta(pagemeta['scheme'], c)['requires'][what]
        gathered.extend([el for el in required if el not in gathered])
    msgr.debug('resolved required contexts ({1}): {0}'.format(gathered, what))
    return gathered

def loadcontexts(path, schemes, scheme, context, required, msgr):
    for element in required:
        if element[0] == '#':
            key, query = tuple(element[1:].split(':', 1))
            msgr.debug('creating context with key "{0}" from query: {1}'.format(key, query))
            got = db.db(path=path).load().rawquery(query=query)
            cntxt = [entry._context for key, entry in got]
            for i, en in enumerate(got):
                en = en[1]
                cntxt[i]['meta'] = en._meta
            cntxt = {key: cntxt}
        else:
            cntxt = json.loads(util.readfile(os.path.join(schemes, scheme, 'elements', element, 'context.json')))
        for k, v in cntxt.items():
            if k in context: msgr.message('warning: key conflict in context: {0}: {1} -> {2}'.format(k, context[k], v))
            context[k] = v
    return context

def loadbasecontexts(path, schemes, scheme, context, required, msgr):
    for element in required:
        if element[0] == '#':
            continue
        conpath = os.path.join(path, '.bearton', 'db', 'base', element, 'context.json')
        if not os.path.isfile(conpath):
            msgr.debug('warning: loading default context for base element: {0}'.format(element))
            conpath = os.path.join(schemes, scheme, 'elements', element, 'context.json')
        cntxt = json.loads(util.readfile(conpath))
        for k, v in cntxt.items():
            if k in context: msgr.message('warning: key conflict in context: {0}: {1} -> {2}'.format(k, context[k], v))
            context[k] = v
    return context

def _getstuff(path, schemes, page, msgr):
    path = os.path.abspath(path)
    dbpath = os.path.join(path, '.bearton', 'db', 'pages')
    pagepath = os.path.join(dbpath, page)
    msgr.debug('schemes: {0}'.format(schemes))
    msgr.debug('path: {0}'.format(path))
    msgr.debug('pagepath: {0}'.format(pagepath))
    meta = json.loads(util.readfile(os.path.join(pagepath, 'meta.json')))
    context = json.loads(util.readfile(os.path.join(pagepath, 'context.json')))
    context = loadcontexts(path, schemes, meta['scheme'], context, gathercontexts(path, pagepath, msgr, 'contexts'), msgr)
    context = loadbasecontexts(path, schemes, meta['scheme'], context, gathercontexts(path, pagepath, msgr, 'base'), msgr)
    template = os.path.join(schemes, meta['scheme'], 'elements', meta['name'], 'template.mustache')
    msgr.debug('reading template: {0}'.format(template))
    template = util.readfile(template)
    return (meta, context, template)

def render(path, schemes, page, msgr):
    meta, context, template = _getstuff(path, schemes, page, msgr)
    lookup = [os.path.join(schemes, meta['scheme'], 'elements'), os.path.join(path, '.bearton', 'db', 'pages', page)]
    parsed = muspyche.parser.parse(template, lookup)
    context = muspyche.context.ContextStack(context)
    renderer = muspyche.renderer.Renderer(parsed, context, lookup)
    if markdown is not None:
        # apply Markdown post-renderer for out-of-the-box Markdown support for
        # Markdown partials (e.g. articles)
        renderer.addpost('^markdown/', markdown.markdown)
    return renderer.render()

def build(path, schemes, page, msgr):
    meta = json.loads(util.readfile(os.path.join(path, '.bearton', 'db', 'pages', page, 'meta.json')))
    output = os.path.join(path, util.expandoutput(meta['output']))
    msgr.debug('written file to: {0}'.format(output))
    util.writefile(output, render(path, schemes, page, msgr))
