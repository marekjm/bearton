"""Various utility functions.
"""


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
