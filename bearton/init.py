"""Module responsible for initilaizing Bearton locals.
"""

import json
import os
import shutil

from . import util
from . import config


REQUIRED_REPO_DIRECTORIES = [
    ('',),
    ('schemes',),
    ('db',),
    ('db', 'pages'),
    ('db', 'base'),
    ('tmp',),
    ('..', 'assets',),
    ('..', 'data',),
]


def _gendirs(target, messenger):
    """Create require directories.
    """
    for parts in REQUIRED_REPO_DIRECTORIES:
        path = os.path.normpath(os.path.join(target, *parts))
        if not os.path.isdir(path):
            if messenger is not None: messenger.debug('creating: {0}'.format(path))
            os.mkdir(path)

def _newconf(target, messenger):
    """Create empty config file.
    """
    cnfg = config.Configuration(target).default().store()
    if messenger is not None: messenger.debug('written default config file to {0}'.format(cnfg._path))

def new(target, messenger=None):
    """Creates a new Bearton local repo.
    """
    _gendirs(target, messenger)
    _newconf(target, messenger)

def update(target, messenger):
    """Updates Bearton repository, e.g. creates new directories required by more recent version of Bearton suite.
    """
    _newdirs(target, messenger)

#def rm(target, msgr):
#   for part in ['assets', 'data']:
#        path = os.path.join(target, part)
#        if os.path.isdir(path):
#            shutil.rmtree(path)
#            if messenger is not None: messenger.debug('removed: {0}'.format(path))
#    path = os.path.join(target, '.bearton')
#    if messenger is not None: messenger.debug('possible Bearton repo in: {0} ({1})'.format(path, os.path.isdir(path)))
#    if os.path.isdir(path):
#        shutil.rmtree(path)
#        if messenger is not None: messenger.message('removed Bearton local from {0}'.format(path), 1)

#def syncschemes(target, schemes, wanted, msgr):
#    for w in wanted:
#        targetpath = os.path.join(target, w)
#        sourcepath = os.path.join(schemes, w)
#        if os.path.isdir(targetpath):
#            if messenger is not None: messenger.message('removing scheme "{0}" from {1}'.format(w, target), 1)
#            shutil.rmtree(targetpath)
#        if messenger is not None: messenger.message('copying scheme "{0}" from {1}'.format(w, schemes), 1)
#        shutil.copytree(sourcepath, targetpath)
