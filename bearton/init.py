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
    ('..', 'assets', 'scheme'),
    ('..', 'assets', 'custom'),
    ('..', 'data',),
    ('..', 'data', 'scheme'),
    ('..', 'data', 'custom'),
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
