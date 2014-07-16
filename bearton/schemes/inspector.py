"""Module responsible for providing information about schemes.
"""

import json
import os

from .. import util


def lselements(scheme):
    """Returns a list of elements of given scheme.
    Parameters:

    - path:     path to the directory scheme is located in,
    - scheme:   name of the scheme,
    """
    return os.listdir(os.path.join(scheme, 'elements'))


def getElementMetas(scheme):
    """Return list of two-tuples: (name, meta).
    """
    path, scheme = os.path.split(scheme)
    elements = lselements(path, scheme)
    metas = []
    for i in elements:
        meta = json.loads(util.io.read(os.path.join(path, scheme, 'elements', i, 'meta.json')))
        metas.append( (i, meta) )
    return metas


def getElementMeta(scheme, element):
    """Returns meta of element in given scheme.
    """
    return json.loads(util.io.read(os.path.join(scheme, 'elements', element, 'meta.json')))


def getSchemePath(scheme, target=None):
    """Returns path to the scheme.
    The `target` parameter point to Bearton repository in which to begin searching.
    If it is None, use util.env functions to find a suitable repository.
    """
    schemes = util.env.listschemes(util.env.getschemespaths(target if target is not None else util.env.getrepopath()))
    candidates = [path for schm, path in schemes if schm == scheme]
    if not candidates: raise FileNotFoundError('could not find a path for scheme: {0}'.format(scheme))
    return os.path.join(candidates[0], scheme)


def getSchemeMeta(scheme):
    """Return meta of whole scheme.
    """
    return json.loads(util.io.read(os.path.join(scheme, 'meta.json')))
