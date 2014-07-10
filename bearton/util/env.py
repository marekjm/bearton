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


def getschemespath(cwd='.'):
    path = ''
    paths = [(cwd, '.bearton', 'schemes'),
             (os.path.expanduser('~'), '.local', 'share', 'bearton', 'schemes'),
             ('/', 'usr', 'share', 'bearton', 'schemes'),
    ]
    for p in paths:
        if os.path.isdir(os.path.join(*p)):
            path = os.path.join(*p)
            break
    return path

def getuipath(cwd=''):
    path = ''
    paths = [(os.path.expanduser('~'), '.local', 'share', 'bearton', 'ui'),
             ('/', 'usr', 'share', 'bearton', 'ui'),
             (cwd, 'ui'),
    ]
    if cwd: paths.insert(0, paths.pop(-1))
    for p in paths:
        if os.path.isdir(os.path.join(*p)):
            path = os.path.join(*p)
            break
    return path

def getuimodel(filename):
    """Takes a filename (from the __file__ of the calling script) and
    returns a tuple: (extracted-filename, ui-model)
    """
    filename = os.path.splitext(os.path.split(filename)[-1])[0]
    uipath = os.path.join(getuipath(), '{0}.clap.json'.format(filename))
    try:
        ifstream = open(uipath, 'r')
        model = json.loads(ifstream.read())
        ifstream.close()
        err = None
    except Exception as e:
        err = e
    finally:
        if err is not None:
            raise type(err)('failed to read UI description located at "{0}": {1}'.format(uipath, err))
    return (filename, model)

def getrepopath(start='.'):
    """Returns path to the bearton repo or empty string if path cannot be found.
    """
    base, path = os.path.abspath(path), ''
    while os.path.split(base)[1] != '':
        path = base[:]
        if os.path.isdir(os.path.join(base, '.bearton')): break
        base, path = os.path.split(base)[0], ''
    if not path: errors.RepositoryNotFound(os.path.abspath(start))
    return path


def inrepo(path='.', panic=False):
    """Returns true if given directory can be used as by Bearton as repository, false otherwise.
    If `panic` parameter is true, will raise exception with appropriate message.
    """
    usable = getrepopath(path) != ''
    if not usable and panic: raise exceptions.BeartonError('"{0}" is not a bearton repository (and no parent is)'.format(os.path.abspath(path)))
    return usable
