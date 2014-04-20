"""Module responsible for applying schems.
"""

import json
import os
import shutil


from .. import util


def _copyassets(source, target, msgr):
    msgr.debug('copying assets...')
    shutil.copytree(os.path.join(source, 'assets'), os.path.join(target, 'assets'))

def _copydata(source, target, msgr):
    msgr.debug('copying data...')
    shutil.copytree(os.path.join(source, 'data'), os.path.join(target, 'data'))

def _makedirs(source, target, msgr):
    meta = json.loads(util.readfile(os.path.join(source, 'meta.json')))
    dirs = (meta['dirs'] if 'dirs' in meta else [])
    msgr.debug('creating {0} directorie(s) required by scheme...'.format(len(dirs)))
    for d in dirs:
        path = os.path.join(target, d)
        if os.path.isdir(path):
            msgr.debug('warning: directory exists: {0}'.format(path))
        else:
            msgr.debug('creating directory: {0}'.format(path))
            os.mkdir(path)

def apply(source, target, msgr):
    msgr.debug('applying scheme: source: {0}'.format(source))
    msgr.debug('applying scheme: target: {0}'.format(target))
    _copyassets(source, target, msgr)
    _copydata(source, target, msgr)
    _makedirs(source, target, msgr)


def _rmdirs(source, target, msgr):
    meta = json.loads(util.readfile(os.path.join(source, 'meta.json')))
    dirs = (meta['dirs'] if 'dirs' in meta else [])
    dirs.reverse()
    msgr.debug('removing {0} directorie(s) required by scheme...'.format(len(dirs)))
    for d in dirs:
        path = os.path.join(target, d)
        if not os.path.isdir(path):
            msgr.debug('warning: directory did not exist: {0}'.format(path))
        else:
            msgr.debug('removing directory: {0}'.format(path))
            shutil.rmtree(path)

def rm(source, target, msgr):
    for i in ['assets', 'data']:
        path = os.path.join(target, i)
        msgr.debug('removing {0} from: {1}'.format(i, path))
        if os.path.isdir(path): shutil.rmtree(path)
        else: msgr.debug('warning: directory does not exist: {0}'.format(path))
    _rmdirs(source, target, msgr)


def lselements(name):
    """Returns a list of elements of given scheme.
    """
    path = os.path.join(util.getschemespath(), name, 'elements')
    return os.listdir(path)

def getElementMetas(scheme):
    """Return list of two-tuples: (name, meta).
    """
    path = os.path.join(util.getschemespath(), scheme, 'elements')
    els = lselements(scheme)
    metas = []
    for i in els:
        meta = json.loads(util.readfile(os.path.join(path, i, 'meta.json')))
        metas.append( (i, meta) )
    return metas

def getMeta(scheme, element):
    """Returns meta of element in given scheme.
    """
    return json.loads(util.readfile(os.path.join(util.getschemespath(), scheme, 'elements', element, 'meta.json')))
