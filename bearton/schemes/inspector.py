"""Module responsible for providing information about schemes.
"""

import json
import os

from .. import util


def lselements(scheme):
    """Returns a list of elements of given scheme.
    """
    path = os.path.join(util.getschemespath(), scheme, 'elements')
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
