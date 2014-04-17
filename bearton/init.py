"""Module responsible for initilaizing Bearton locals.
"""

import json
import os
import shutil

from . import util
from . import config


def _newdirs(target, msgr):
    """Create require directories.
    """
    dirs = [('.bearton',),
            ('.bearton', 'schemes'),
            ('.bearton', 'db'),
            ('.bearton', 'db', 'pages'),
            ('.bearton', 'db', 'base'),
            ('assets',),
            ('data',),
            ]
    for parts in dirs:
        path = os.path.join(target, *parts)
        os.mkdir(path)
        msgr.debug('creating: {0}'.format(path), 2)

def _newconf(target, msgr):
    """Create empty config file.
    """
    config.Configuration(os.path.join(target, '.bearton', 'config.json')).default().store().unload()
    msgr.debug('written default config file to {0}'.format(os.path.join(target, '.bearton')))

def _copyschemes(target, schemes_path, msgr):
    """Copy schemes to new Bearton local site repository.
    """
    msgr.debug('schemes are copied from: {0}'.format(schemes_path))
    for scheme in os.listdir(schemes_path): shutil.copytree(os.path.join(schemes_path, scheme), os.path.join(target, '.bearton', 'schemes', scheme))

def new(target, schemes='', msgr=None):
    """Creates a new Bearton local repo.
    """
    if not os.path.isdir(target): raise NotADirectoryError(target)
    _newdirs(target, msgr)
    _newconf(target, msgr)
    if schemes: _copyschemes(target, schemes, msgr)

def rm(target, msgr):
    for part in ['assets', 'data']:
        path = os.path.join(target, part)
        if os.path.isdir(path):
            shutil.rmtree(path)
            msgr.debug('removed: {0}'.format(path))
    path = os.path.join(target, '.bearton')
    msgr.debug('possible Bearton repo in: {0} ({1})'.format(path, os.path.isdir(path)))
    if os.path.isdir(path):
        shutil.rmtree(path)
        msgr.message('removed Bearton local from {0}'.format(path), 0)

def syncschemes(target, schemes, wanted, msgr):
    for w in wanted:
        targetpath = os.path.join(target, w)
        sourcepath = os.path.join(schemes, w)
        if os.path.isdir(targetpath):
            msgr.message('removing scheme "{0}" from {1}'.format(w, target), 1)
            shutil.rmtree(targetpath)
        msgr.message('copying scheme "{0}" from {1}'.format(w, schemes), 1)
        shutil.copytree(sourcepath, targetpath)
