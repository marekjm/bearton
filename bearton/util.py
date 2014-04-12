"""Various utility functions.
"""


import sys


class Messenger:
    """Object used to display messages, i.e. print them to console.
    """
    def __init__(self, verbosity=0, quiet=False, debugging=False, stream=sys.stdout):
        self._verbosity = verbosity
        self._quiet = quiet
        self._debugging = debugging
        self._stream = stream

    def setVerbosity(self, n):
        self._vebrosity = n

    def message(self, msg, verbosity=0):
        """Write message to stream.
        """
        if self._quiet: return
        if self._verbosity < verbosity: return
        msg = '{0}\n'.format(msg)
        self._stream.write(msg)

    def debug(self, msg):
        """Write debug message to stream.
        """
        msg = 'debug: {0}\n'.format(msg)
        if self._debugging: self._stream.write(msg)


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
