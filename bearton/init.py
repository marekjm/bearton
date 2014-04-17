"""Module responsible for initilaizing Bearton locals.
"""

import json
import os
import shutil

from . import util
from . import config


def _newdirs(target, msgr=None):
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
        if msgr is not None: msgr.message('creating: {0}'.format(path), 2)

def _newconf(target, msgr):
    """Create empty config file.
    """
    config = config.Configuration(os.path.join(target, '.bearton')).load().default().store().unload()
    msgr.message('written default config file to {0}'.format(config_path), 1)

def _copyschemes(target, schemes_path, msgr):
    """Copy schemes to new Bearton local site repository.
    """
    msgr.message('target: {0}'.format(target))
    msgr.message('schemes: {0}'.format(schemes_path))
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
            msgr.message('removed: {0}'.format(path), 2)
    path = os.path.join(target, '.bearton')
    if os.path.isdir(path):
        shutil.rmtree(path)
        msgr.message('removed Bearton local from {0}'.format(path), 1)

def syncschemes(target, schemes, wanted, msgr):
    for w in wanted:
        targetpath = os.path.join(target, w)
        sourcepath = os.path.join(schemes, w)
        if os.path.isdir(targetpath):
            msgr.debug('removing scheme "{0}" from {1}'.format(w, target))
            shutil.rmtree(targetpath)
        msgr.debug('copying scheme "{0}" from {1}'.format(w, schemes))
        shutil.copytree(sourcepath, targetpath)
