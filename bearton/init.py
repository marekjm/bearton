"""Module responsible for initilaizing Bearton locals.
"""

import os

def inside(where):
    if not os.path.isdir(where): raise NotADirectoryError(where)

def outside(where):
    if not os.path.isdir(where): raise NotADirectoryError(where)
