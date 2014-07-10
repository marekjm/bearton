"""Utility functions related to IO operations preformed by Bearton.
"""

import os


def read(path, encoding='utf-8', default=None):
    """Reads a file as bytes.
    Returns string decoded with given encoding.
    If encoding is None returns raw bytes.
    """
    if not os.path.isfile(path) and default is not None: return default
    ifstream = open(path, 'rb')
    s = ifstream.read()
    ifstream.close()
    if encoding is not None: s = s.decode(encoding)
    return s

def write(path, s, encoding='utf-8'):
    """Writes a file.
    By default, writes as bytes.
    To write as string, pass `encoding` as None.
    """
    ofstream = open(path, ('wb' if encoding is not None else 'w'))
    if encoding is not None: s = s.encode(encoding)
    ofstream.write(s)
    ofstream.close()
