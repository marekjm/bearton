import json
import os
import sys

import muspyche

from .. import util
from .. import conf


class Element:
    """Class used to build objects.
    """
    def __init__(self, scheme, element):
        self._scheme = scheme
        self._element = element
        self._template, self._context = '', {}
        self._meta = {}

    def _loadtemplate(self, schemepath):
        elpath = os.path.join(schemepath, 'elements', self._element)
        tmplt = util.readfile(os.path.join(elpath, 'template.mustache'))
        self._template = muspyche.parser.parse(tmplt, lookup=[elpath, os.path.join(schemepath, 'elements')])

    def _loadcontext(self, schemepath):
        elpath = os.path.join(schemepath, 'elements', self._element)
        cntxt = util.readfile(os.path.join(elpath, 'context.json'))
        self._context = json.loads(cntxt)

    def _loadmeta(self, schemepath):
        elpath = os.path.join(schemepath, 'elements', self._element)
        meta = util.readfile(os.path.join(elpath, 'meta.json'))
        self._meta = json.loads(meta)

    def load(self):
        """Loads element's template, context and metadata.
        """
        schemepath = os.path.join('schemes', conf.Configuration().load().get('scheme'))
        self._loadtemplate(schemepath)
        self._loadcontext(schemepath)
        self._loadmeta(schemepath)
        return self

    def _gathercontexts(self, schemepath):
        print(self._meta['requires']['contexts'])

    def prepare(self):
        """Prepares element's elements.
        """
        schemepath = os.path.join('schemes', conf.Configuration().load().get('scheme'))
        self._gathercontexts(schemepath)
        return self
