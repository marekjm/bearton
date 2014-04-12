import base64
import hashlib
import os

from . import util
from . import config


def new(site, scheme, element):
    hashed = hashlib.sha256(base64.b64encode(os.urandom(64))).hexdigest()
    print(hashed)
    print(site, os.path.isdir(site))
    beartonrepo = os.path.join(site, '.bearton')
    print()
