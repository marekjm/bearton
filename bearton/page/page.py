"""Bearton module providing functions that deal with pages.
"""

import base64
import hashlib
import os
import shutil

from .. import util
from .. import config
from .. import db


def new(target, use, messenger=None):
    """Create new page using <use> data and
    place it in the database inside <target> repository.
    Use <messenger> for reporting.

    The `use` parameter is a two-tuple: (scheme-directory, element-name)
    """
    scheme, element = use
    element_path = os.path.join(scheme, 'elements', element)
    if messenger is not None: messenger.debug('reading element data from: {0}'.format(element_path))
    hashed = hashlib.sha256(base64.b64encode(os.urandom(64))).hexdigest()
    if messenger is not None: messenger.debug('setting unique id (database key) for new page: {0}'.format(hashed))
    hashpath = os.path.join(target, 'db', 'pages', hashed)
    if messenger is not None: messenger.debug('creating databse entry: {0}'.format(hashpath))
    os.mkdir(hashpath)
    for d in ['markdown']:
        mkpath = os.path.join(hashpath, d)
        os.mkdir(mkpath)
    for f in ['meta', 'context', 'hints']:
        f += '.json'
        if messenger is not None: messenger.debug('copying {0}'.format(f), keep=True)
        if messenger is not None: messenger.onok(msg='\tOK').onfail(msg='\tFAIL: {:error_msg}')
        if messenger is not None: messenger.call(shutil.copy, os.path.join(element_path, f), os.path.join(hashpath, f))
        if messenger is not None: messenger.report()
    entry = db.Entry(*os.path.split(hashpath)).load()
    if 'scheme' not in entry._meta: entry.setinmeta('scheme', os.path.split(scheme)[1])
    if 'name' not in entry._meta: entry.setinmeta('name', element)
    entry.setinmeta('output', util.env.expandoutput(entry.metag('output')))
    entry.store()
    return hashed

def newbase(target, use, messenger=None):
    """Create new page using <use> data and
    place it in the database inside <target> repository.
    Use <messenger> for reporting.

    The `use` parameter is a two-tuple: (scheme-directory, element-name)
    """
    scheme, element = use
    basepath = os.path.join(target, 'db', 'base', element)
    os.mkdir(basepath)
    files = ['meta', 'context', 'hints']
    element_path = os.path.join(scheme, 'elements', element)
    for f in files:
        f += '.json'
        if messenger is not None: messenger.debug('copying {0}'.format(f), keep=True)
        if messenger is not None: messenger.onok(msg='\tOK').onfail(msg='\tFAIL: {:error_msg}')
        if messenger is not None: messenger.call(shutil.copy, os.path.join(element_path, f), os.path.join(basepath, f))
        if messenger is not None: messenger.report()

def edit(path, page, base, messenger=None):
    """Launches editor to edit context of given page.
    """
    path = os.path.abspath(os.path.join(path, '.bearton', 'db', ('base' if base else 'pages'), page, 'context.json'))
    editcmd = '{0} "{1}"'.format(os.getenv('EDITOR', 'vim'), path)
    if messenger is not None: messenger.debug(editcmd)
    if os.path.isfile(path):
        ok = True
        os.system(editcmd)
    else:
        ok = False
    return ok

def editmarkdown(path, page, element, messenger=None):
    """Lanuches editor to edit Markdown partials of given page.
    """
    base = os.path.abspath(os.path.join(path, '.bearton', 'db', 'pages', page, 'markdown'))
    path = ''
    for i in ['{0}', '{0}.md', '{0}.markdown']:
        candidate = os.path.join(base, i.format(element))
        if os.path.isfile(candidate):
            path = candidate
            break
    editcmd = '{0} "{1}"'.format(os.getenv('EDITOR', 'vim'), path)
    if messenger is not None: messenger.debug(editcmd)
    if path:
        ok = True
        os.system(editcmd)
    else:
        ok = False
    return ok
