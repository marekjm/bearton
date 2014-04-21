"""Various utility functions.
"""


import os
import re
import sys
import time


class Messenger:
    """Object used to write messages to stream-like objects.
    """
    def __init__(self, verbosity=0, quiet=False, debugging=False, stream=sys.stdout):
        self._stream = stream
        self._verbosity = verbosity
        self._quiet, self._debugging = quiet, debugging
        self._line, self._lineend = '', '\n'
        self._on = {}
        err = None
        try:
            stream.write
        except Exception as e:
            err = e
        finally:
            if err is not None: raise TypeError('"{0}" is not a valid stream type for Messenger: caused by {1}'.format(str(type(stream))[8:-2], str(type(err))[8:-2]))

    def _send(self, line, keep=False):
        self._line += line
        if not keep:
            self._stream.write(self._line + self._lineend)
            self._line = ''

    def setlineending(self, ending='\n'):
        self._lineend = ending
        return self

    def message(self, msg, verbosity=0, keep=False):
        """Write message to stream.
        """
        if self._quiet: return
        if self._verbosity < verbosity: return
        self._send(msg, keep)
        return self

    def debug(self, msg, keep=False):
        """Write debug message to stream.
        """
        msg = '{0}{1}'.format(('debug: ' if not self._line else ''), msg)
        if self._debugging: self._send(msg, keep)
        return self

    def onok(self, msg):
        self._on['ok'] = msg
        return self

    def onfail(self, msg):
        self._on['fail'] = msg
        return self

    def call(self, callable, *args, **kwargs):
        try:
            callable(*args, **kwargs)
            self.debug(msg=self._on['ok'], keep=True)
        except Exception as e:
            self.debug(msg=self._on['fail'].replace('{:error_msg}', str(e)).replace('{:error_type', str(type(e))[8:-2]), keep=True)
        finally:
            pass

    def report(self):
        self._on = {}
        self.debug('')


def readfile(path, encoding='utf-8'):
    """Reads a file as bytes.
    Returns string decoded with given encoding.
    If encoding is None returns raw bytes.
    """
    ifstream = open(path, 'rb')
    s = ifstream.read()
    ifstream.close()
    if encoding is not None: s = s.decode(encoding)
    return s

def writefile(path, s, encoding='utf-8'):
    """Writes a file.
    By default, writes as bytes.
    To write as string, pass `encoding` as None.
    """
    ofstream = open(path, ('wb' if encoding is not None else 'w'))
    if encoding is not None: s = s.encode(encoding)
    ofstream.write(s)
    ofstream.close()


def expandoutput(s):
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
    regex_key = re.compile('{:([a-zA-Z-_]+)}')
    keys = regex_key.findall(s)
    for key in keys:
        value = input('{0}: '.format(key))
        s = s.replace(('{:'+key+'}'), value)
    return s


def dictsimilarise(base, update):
    """Copies keys missing in base but present in update to base dictionary.
    Does not overwrite or update any value already present in base.

    Raises TypeError when the same key has different type in base and update dicts.
    """
    new = {}
    for k, v in base.items(): new[k] = v
    for key in update:
        if key in base:
            if type(base[key]) != type(update[key]):
                raise TypeError('different types for key: {0}'.format(key))
            if type(base[key]) == dict:
                new[key] = dictsimilarise(base[key], update[key])
        else:
            new[key] = update[key]
    return new

def dictupdate(base, update, overwrites=True, allow_ow=[], removals=True):
    """Updates all values present in base with values present in update.
    If `removals` is true, removes all keys that are not present in update.
    Else, leaves them as they were.
    `allow_ow` is a list of keys for which aoverwrites are allowed.
    """
    new = {}
    for key in base:
        if key in update:
            if overwrites or key in allow_ow:
                if type(base[key]) == dict and type(update[key]) == dict: value = dictupdate(base[key], update[key], overwrites, allow_ow, removals)
                else: value = update[key]
            else: value = base[key]
            new[key] = value
        if key not in update and not removals:
            new[key] = base[key]
    return new

def dictmerge(base, update, **kwargs):
    """First similarises and then updates base dict with update dict.
    kwargs are passed to dictupdate() function and are not directly used by dictmerge.
    """
    new = dictupdate(base=dictsimilarise(base, update), update=update, **kwargs)
    return new


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
