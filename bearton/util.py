"""Various utility functions.
"""


import sys
import time


class Messenger:
    """Object used to display messages, i.e. print them to console.
    """
    def __init__(self, verbosity=0, quiet=False, debugging=False, stream=sys.stdout):
        self._stream = stream
        self._verbosity = verbosity
        self._quiet, self._debugging = quiet, debugging
        self._line, self._lineend = '', '\n'
        self._on = {}

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
    """
    ofstream = open(path, 'wb')
    if encoding is not None: s = s.encode(encoding)
    ofstream.write(s)

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
        s = s.replace(('{{'+key+'}}'), str(value))
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
        if key not in base:
            if type(base[key]) == dict:
                value = dictsimilarise(base[key], update[key])
            else:
                value = update[key]
            new[key] = value
    return new

def dictupdate(base, update, removals=True):
    """Updates all values present in base with values present in update.
    If `removals` is true, removes all kes that are not prsent in update.
    Else, leaves them as they were.
    """
    new = {}
    for key in base:
        if key in update: new[key] = update[key]
        elif key not in update and not removals: new[key] = base[key]
    return new

def dictmerge(base, update):
    """First similarises and then updates (with removals) ase dict with update dict.
    """
    #print('base:', base)
    #print('update:', update)
    new = dictupdate(dictsimilarise(base, update), update)
    #print('new:', new)
    return new
