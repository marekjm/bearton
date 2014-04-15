import base64
import hashlib
import os
import shutil

from .. import util
from .. import config


def new(path, schemes_path, scheme, element, msgr=None, what='pages'):
    hashed = hashlib.sha256(base64.b64encode(os.urandom(64))).hexdigest()
    if msgr is not None: msgr.debug(hashed)
    if msgr is not None: msgr.debug('{0} {1}'.format(path, os.path.isdir(path)))
    hashpath = os.path.join(path, '.bearton', 'db', what, hashed)
    msgr.debug('creating databse entry: {0}'.format(hashpath))
    os.mkdir(hashpath)
    files = ['meta', 'context', 'hints']
    element_path = os.path.join(schemes_path, scheme, 'elements', element)
    for f in files:
        f += '.json'
        msgr.debug('copying {0}'.format(f), keep=True)
        msgr.onok(msg='\tOK').onfail(msg='\tFAIL: {:error_msg}')
        msgr.call(shutil.copy, os.path.join(element_path, f), os.path.join(hashpath, f))
        msgr.report()
    return hashed

def edit(path, page, msgr=None):
    msgr.debug('editing in: {0}'.format(path))
    path = os.path.join(path, '.bearton', 'db')
    msgr.debug('path to database: {0} ({1})'.format(path, ('OK' if os.path.isdir(path) else 'FAIL')))
    msgr.debug('editing page: {0} ({1})'.format(page, ('OK' if os.path.isdir(os.path.join(path, page)) else 'FAIL')))
