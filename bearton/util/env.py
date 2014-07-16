"""Utility functions dealing with Bearton environment.
"""

import json
import os
import re
import sys
import time

try: import readline
except ImportError: pass # These are not the modules you're looking for... Move along. (The OS is most probably Windows in such case.)
finally: pass

from bearton import errors


SHARED_RESOURCES_LOCATIONS = [
    ('.',),
    (os.path.expanduser('~'), '.local', 'share', 'bearton'),
    ('/', 'usr', 'share', 'bearton'),
]


def expandoutput(s):
    """Expand output path, replacing every variable found in it with its value.
    If a value is not found in the dictionary, user is asked to provide it.
    """
    epoch = time.time()
    struct_tm = time.gmtime(epoch)
    context = {'year': struct_tm.tm_year,
               'month': struct_tm.tm_mon,
               'mday': struct_tm.tm_mday,
               'yday': struct_tm.tm_yday,
               'epoch': epoch,
               }
    for key, value in context.items():
        s = s.replace(('{:'+key+'}'), str(value))
    regex_key = re.compile('{:([a-zA-Z][a-zA-Z-_]+[a-zA-Z])}')
    keys = regex_key.findall(s)
    for key in keys:
        value = input('{0}: '.format(key))
        s = s.replace(('{:'+key+'}'), value)
    return s


def getrepopath(start='.', nofail=False):
    """Returns path to the Bearton repo.
    Raises exception if repository cannot be found.
    """
    base, path = os.path.abspath(start), ''
    while os.path.split(base)[1] != '':
        path = base[:]
        if os.path.isdir(os.path.join(base, '.bearton')): break
        base, path = os.path.split(base)[0], ''
    if not path and not nofail: raise errors.RepositoryNotFoundError(os.path.abspath(start))
    return os.path.join((path if path else start), '.bearton')


def getresourcelocations():
    """Returns list of locations where Bearton shared resources can be found.
    """
    paths = [os.path.join(*i) for i in SHARED_RESOURCES_LOCATIONS]
    return paths


def getschemespaths(repo='.'):
    """Returns list of possible schemes locations.
    """
    paths = getresourcelocations()
    if repo: paths.insert(0, os.path.join(getrepopath(start=repo, nofail=True)))
    paths = [os.path.join(i, 'schemes') for i in paths]
    paths = [i for i in paths if os.path.isdir(i)]
    return paths

def listschemes(scheme_paths):
    """List all available schemes in all locations.
    """
    schemes = []
    for path in scheme_paths:
        ls = os.listdir(path)
        for schm in ls: schemes.append( (schm, path) )
    return schemes

def _getuilocations():
    """Returns list of possible UI locations.
    """
    paths = getresourcelocations()
    paths = [os.path.join(i, 'ui') for i in paths]
    return paths

def getuipath():
    """Return path to UI descriptions directory.
    Raise exception if not found.
    """
    path = ''
    paths = _getuilocations()
    for p in paths:
        if os.path.isdir(p):
            path = p
            break
    if not path: raise errors.UIDescriptionsNotFoundError()
    return path

def getuimodel(ui):
    """Takes a filename and returns a tuple: (path-to-ui-description, ui-model)
    """
    path = os.path.join(getuipath(), '{0}.clap.json'.format(ui))
    try:
        ifstream = open(path, 'r')
        model = json.loads(ifstream.read())
        ifstream.close()
        err = None
    except Exception as e:
        err = e
    finally:
        if err is not None:
            raise type(err)('failed to read UI description located at "{0}": {1}'.format(path, err))
    if not path: raise errors.UIDescriptionsNotFoundError(ui)
    return model
