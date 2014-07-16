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
        self._callerror, self._on = None, {'ok': '', 'fail': ''}
        self._indent = {'level': 0, 'string': '    '}
        self._buffer, self._buffered = False, []
        err = None
        try:
            stream.write
        except Exception as e:
            err = e
        finally:
            if err is not None: raise TypeError('"{0}" is not a valid stream type for Messenger: caused by {1}'.format(str(type(stream))[8:-2], str(type(err))[8:-2]))

    def _send(self, line, keep=False):
        """Write line to output stream.
        If keep is true, append to internal line instead of writing to the output.
        """
        self._line += line
        if not keep:
            line = self._indent['level'] * self._indent['string']
            line += self._line + self._lineend
            if self._buffer: self._buffered.append(line)
            else: self._stream.write(line)
            self._line = ''

    def setVerbosity(self, level=1):
        """Sets verbosity level (integer).
        """
        self._verbosity = level
        return self

    def setDebug(self, enabled=True):
        """Set debug output to enabled or disabled.
        """
        self._debugging = enabled
        return self

    def setlineending(self, ending='\n'):
        self._lineend = ending
        return self

    def message(self, msg, verbosity=0, max_verbosity=None, keep=False):
        """Write message to stream.
        """
        if self._quiet: return
        if self._verbosity < verbosity: return
        if max_verbosity is not None and self._verbosity > max_verbosity: return
        self._send(msg, keep)
        return self

    def debug(self, msg, keep=False):
        """Write debug message to stream.
        """
        msg = '{0}{1}'.format(('debug: ' if not self._line else ''), msg)
        if self._debugging: self._send(msg, keep)
        return self

    def warn(self, msg, keep=False):
        """Write warning message to stream.
        """
        msg = '{0}{1}'.format(('warning: ' if not self._line else ''), msg)
        self._send(msg, keep)
        return self

    def note(self, msg, keep=False):
        """Write note message to stream.
        """
        msg = '{0}{1}'.format(('note: ' if not self._line else ''), msg)
        self._send(msg, keep)
        return self

    def onok(self, msg):
        """Set message to be displayed if .call() will not result in error.
        """
        self._on['ok'] = msg
        return self

    def onfail(self, msg):
        """Set message to be displayed if .call() will result in error.
        """
        self._on['fail'] = msg
        return self

    def call(self, callable, *args, **kwargs):
        """Call callable and, depending on whether it raises an exception or not, set correct report message.
        This function returns whatever value the `callable` returned.
        By default .call() returns None.
        In case of exception being raised by `callable`, .call() returns None.
        """
        result = None
        try:
            result = callable(*args, **kwargs)
            self.debug(msg=self._on['ok'], keep=True)
        except Exception as e:
            self.debug(msg=self._on['fail'].replace('{:error_msg}', str(e)).replace('{:error_type', str(type(e))[8:-2]), keep=True)
        finally:
            pass
        return result

    def report(self):
        """Call this method after .call() to display report message.
        Reporting is done on the "debug" channel.
        """
        self._on = {'ok': '', 'fail': ''}
        self._callerror = None
        self.debug('')
        return self

    def indent(self):
        """Increase indentation level of output.
        """
        self._indent['level'] += 1
        return self

    def dedent(self):
        """Increase indentation level of output.
        """
        self._indent['level'] -= 1
        return self

    def buffer(self, enabled):
        """Switch buffering state.
        If `enabled` is true - enable, otherwise disable the buffer.
        """
        self._buffer = enabled
        return self

    def push(self):
        """Send buffer contents to output stream.
        """
        state = int(self._buffer)
        self.buffer(False)
        for i in self._buffered: self._send(i)
        self.buffer(bool(state)) # to prevent enabling buffer if it was disabled in the first place
        self.clear()
        return self

    def wipe(self):
        """Wipe buffer contents.
        """
        self._buffered = []
        return self
