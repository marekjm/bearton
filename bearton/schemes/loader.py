"""Module responsible for applying schems.
"""

import json
import os
import shutil

from .. import util


def _copyassets(source, target, messenger=None):
    """Copy media assets that come with the scheme.
    """
    src = os.path.join(source, 'assets')
    trgt = os.path.join(target, 'assets', 'scheme')
    if messenger is not None:
        messenger.debug('copying assets: source: {0}'.format(src))
        messenger.debug('copying assets: target: {0}'.format(trgt))
    if os.path.isdir(trgt): shutil.rmtree(trgt)
    shutil.copytree(src, trgt)

def _copydata(source, target, messenger=None):
    """Copy data (CSS, JavaScript, JSON, etc.) that come with the scheme.
    """
    src = os.path.join(source, 'data')
    trgt = os.path.join(target, 'data', 'scheme')
    if messenger is not None:
        messenger.debug('copying data: source: {0}'.format(src))
        messenger.debug('copying data: target: {0}'.format(trgt))
    if os.path.isdir(trgt): shutil.rmtree(trgt)
    shutil.copytree(src, trgt)

def _makedirs(source, target, messenger=None):
    """Create all directories required by the scheme.
    """
    meta = json.loads(util.io.read(os.path.join(source, 'meta.json')))
    dirs = (meta['dirs'] if 'dirs' in meta else [])
    if messenger is not None: messenger.debug('creating {0} directorie(s) required by scheme...'.format(len(dirs)))
    for d in dirs:
        path = os.path.join(target, d)
        if os.path.isdir(path):
            if messenger is not None: messenger.debug('warning: directory exists: {0}'.format(path))
        else:
            if messenger is not None: messenger.debug('creating directory: {0}'.format(path))
            os.mkdir(path)

def apply(source, target, messenger=None):
    """Apply scheme to current page.
    """
    if messenger is not None: messenger.debug('applying scheme: source: {0}'.format(source))
    if messenger is not None: messenger.debug('applying scheme: target: {0}'.format(target))
    _copyassets(source, target, messenger)
    _copydata(source, target, messenger)
    _makedirs(source, target, messenger)
