"""Module responsible for initilaizing Bearton locals.
"""

import os
import shutil

from . import util


def _newdirs(where, msgr=None):
    """Create require directories.
    """
    dirs = [('.bearton',),
            ('.bearton', 'schemes'),
            ('.bearton', 'db'),
            ('assets',),
            ('data',),
            ]
    for parts in dirs:
        path = os.path.join(where, *parts)
        os.mkdir(path)
        if msgr is not None: msgr.message('creating: {0}'.format(path), 2)

def _newconf(where, msgr):
    """Create empty config file.
    """
    config_path = os.path.join(where, '.bearton', 'config.json')
    util.writefile(config_path, '{}')
    if msgr is not None: msgr.message('written empty config file to {0}'.format(config_path), 1)

def _copyschemes(where, schemes_path, msgr):
    """Copy schemes to new Bearton local site repository.
    """
    msgr.debug('TODO: implement me!')
    raise

def new(where, schemes='', msgr=None):
    """Creates a new Bearton local repo.
    """
    if not os.path.isdir(where): raise NotADirectoryError(where)
    _newdirs(where, msgr)
    _newconf(where, msgr)
    if schemes: _copyschemes(where, schemes, msgr)

def rm(where, msgr=None):
    for part in ['assets', 'data']:
        path = os.path.join(where, part)
        if os.path.isdir(path):
            shutil.rmtree(path)
            if msgr is not None: msgr.message('removed: {0}'.format(path), 2)
    path = os.path.join(where, '.bearton')
    if os.path.isdir(path):
        shutil.rmtree(path)
        if msgr is not None: msgr.message('removed Bearton local from {0}'.format(path), 1)
