"""Module containing messenger object.
"""

import sys


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
