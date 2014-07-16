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


def gathercontexts(path, pagepath, pagemeta, what='base', messenger=None):
    """Gather all contexts required by the page.
    This function will resolve context dependencies.
    """
    gathered = (pagemeta['requires'][what][:] if what in pagemeta['requires'] else [])
    if messenger is not None:
        messenger.debug('directly required contexts ({0}) for element "{1}": {2}'.format(what, pagemeta['name'], ', '.join(gathered)))
        messenger.indent()
    for c in gathered:
        if c[0] in ['#', '?']:
            required = [c]
        else:
            cmeta = schemes.inspector.getElementMeta(schemes.inspector.getSchemePath(pagemeta['scheme'], path), c)
            has = (what in cmeta['requires'])
            required = (cmeta['requires'][what] if has else [])
            if messenger is not None and required: messenger.debug('dependency contexts required by element "{0}": {1}'.format(c, ', '.join(required)))
        gathered.extend([el for el in required if el not in gathered])
    if messenger is not None:
        messenger.dedent()
        messenger.debug('resolved required contexts ({0}) for element "{1}": {2}'.format(what, pagemeta['name'], ', '.join(gathered)))
    return gathered


def _mergecontexts(context, update, messenger=None):
    """Merges two contexts together.
    """
    for k, v in update.items():
        if k in context and messenger is not None: messenger.message('warning: key conflict in context, leaving: {0}: {1} -> {2}'.format(k, context[k], v))
        context[k] = v
    return context


def loadcontexts(path, scheme, context, required, messenger=None):
    """Loads required additional contexts for requested page.
    """
    # iterate over required elements, they tell us what additional contexts must be loaded
    for element in required:
        if element[0] in ['#', '?']:    # if element begins with # or ? it is a query to be run to get context out od the database
            key, query = tuple(element[1:].split(':', 1)) # set result of the query to the given key
            if messenger is not None: messenger.debug('creating context with key "{0}" from query: {1}'.format(key, query))
            got = db.db(path=path).load().rawquery(query=query)
            # extract contexts out of the query result
            cntxt = [entry._context for key, entry in got]
            # add metadata of queried-out elements to the context
            for i, en in enumerate(got): cntxt[i]['meta'] = en[1]._meta
            cntxt = {key: cntxt}
        else:                           # otherwise, just load the default context for this element (from scheme)
            cntxt = json.loads(util.readfile(os.path.join(scheme, 'elements', element, 'context.json')))
        context = _mergecontexts(context, cntxt, messenger)
    return context


def loadbasecontexts(target, scheme, context, required, messenger):
    """Loads required additional contexts for requested page.
    """
    for element in required:
        if element[0] in ['#', '?']: raise TypeError('queries cannot be used to load base contexts: {0}'.format(element))
        path = os.path.join(target, 'db', 'base', element, 'context.json')
        if not os.path.isfile(path):
            if messenger is not None: messenger.debug('warning: loading default context for base element: {0}'.format(element))
            path = os.path.join(scheme, 'elements', element, 'context.json')
        cntxt = json.loads(util.io.read(path))
        context = _mergecontexts(context, cntxt, messenger)
    return context


def _getstuff(path, schemes, page, msgr):
    raise Exception('FIXME,DOCME')
    path = os.path.abspath(path)
    dbpath = os.path.join(path, '.bearton', 'db', 'pages')
    pagepath = os.path.join(dbpath, page)
    msgr.debug('schemes: {0}'.format(schemes))
    msgr.debug('path: {0}'.format(path))
    msgr.debug('pagepath: {0}'.format(pagepath))
    meta = json.loads(util.readfile(os.path.join(pagepath, 'meta.json')))
    context = json.loads(util.readfile(os.path.join(pagepath, 'context.json')))
    template = os.path.join(schemes, meta['scheme'], 'elements', meta['name'], 'template.mustache')
    msgr.debug('reading template: {0}'.format(template))
    template = util.readfile(template)
    return (meta, context, template)


def _getmeta(pagepath, messenger=None):
    """Returns metadata of the requested page.
    """
    meta = json.loads(util.io.read(os.path.join(pagepath, 'meta.json')))
    return meta


def _getcontext(path, pagepath, meta, messenger=None):
    """Returns context of the requested page.
    """
    context = json.loads(util.io.read(os.path.join(pagepath, 'context.json')))
    scheme_name = (meta['scheme'] if 'scheme' in meta else 'default')
    if messenger is not None: messenger.debug('defined scheme used: {0}'.format(scheme_name))
    scheme_path = [path for schm, path in util.env.listschemes(util.env.getschemespaths()) if schm == scheme_name][0]
    if messenger is not None: messenger.debug('defined scheme path: {0}'.format(scheme_path))
    scheme = os.path.join(scheme_path, scheme_name)
    context = loadcontexts(path, scheme, context, gathercontexts(path, pagepath, meta, 'contexts', messenger), messenger)
    context = loadbasecontexts(path, scheme, context, gathercontexts(path, pagepath, meta, 'base', messenger), messenger)
    return context


def render(target, page, messenger):
    """Renders selected page and returns it as string.
    Parameters:

    *   target: path to the repository,
    *   use:    three-tuple, (
    """
    #meta, context, template = _getstuff(path, schemes, page, msgr)
    #lookup = [os.path.join(schemes, meta['scheme'], 'elements'), os.path.join(path, '.bearton', 'db', 'pages', page)]
    #parsed = muspyche.parser.parse(template, lookup)
    #context = muspyche.context.ContextStack(context)
    #renderer = muspyche.renderer.Renderer(parsed, context, lookup)
    #if markdown is not None:
        # apply Markdown post-renderer for out-of-the-box Markdown support for
        # Markdown partials (e.g. articles written in Markdown)
    #    renderer.addpost('^markdown/', markdown.markdown)
    #return renderer.render()
    pagepath = os.path.join(target, 'db', 'pages', page)
    if messenger is not None: messenger.debug('rendering: set pagepath: {0}'.format(pagepath))
    meta = _getmeta(pagepath, messenger)
    if messenger is not None: messenger.debug('rendering: got metadata')
    context = _getcontext(path=target, pagepath=pagepath, meta=meta, messenger=messenger)
    if messenger is not None: messenger.debug('rendering: got context')
    rendered = ''
    return rendered

def build(path, schemes, page, msgr):
    """Parameters:
    *   target: target directory of the build not repo,
    *   path:   path to scheme directory,
    *   page:   page id to render,
    """
    raise Exception('FIXME,DOCME')
    meta = json.loads(util.readfile(os.path.join(path, '.bearton', 'db', 'pages', page, 'meta.json')))
    output = os.path.join(path, util.expandoutput(meta['output']))
    msgr.debug('written file to: {0}'.format(output))
    util.writefile(output, render(path, schemes, page, msgr))
