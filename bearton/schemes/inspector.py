"""Module responsible for providing information about schemes.
"""

import json
import os

from .. import util


def lselements(path, scheme):
    """Returns a list of elements of given scheme.
    Parameters:

    - path:     path to the directory scheme is located in,
    - scheme:   name of the scheme,
    """
    return os.listdir(os.path.join(path, scheme, 'elements'))

def getElementMetas(scheme):
    """Return list of two-tuples: (name, meta).
    """
    path = os.path.join(scheme, 'elements')
    elements = lselements(scheme)
    metas = []
    for i in elements:
        meta = json.loads(util.io.read(os.path.join(path, i, 'meta.json')))
        metas.append( (i, meta) )
    return metas

def getElementMeta(path, scheme, element):
    """Returns meta of element in given scheme.
    """
    return json.loads(util.io.read(os.path.join(path, scheme, 'elements', element, 'meta.json')))

def getSchemeMeta(scheme):
    """Return meta of whole scheme.
    """
    return json.loads(util.io.read(os.path.join(scheme, 'meta.json')))
