#!/usr/bin/env python3

import json
import os
from sys import argv

import clap
import muspyche

import bearton


# Obtaining requred filename and model
_file = os.path.splitext(os.path.split(__file__)[1])[0]
model = bearton.util.env.getuimodel(_file)

# Building UI
argv = list(clap.formatter.Formatter(argv[1:]).format())
command = clap.builder.Builder(model).insertHelpCommand().build().get()
parser = clap.parser.Parser(command).feed(argv)

try:
    clap.checker.RedChecker(parser).check()
    fail = False
except clap.errors.MissingArgumentError as e:
    print('missing argument for option: {0}'.format(e))
    fail = True
except clap.errors.UnrecognizedOptionError as e:
    print('unrecognized option found: {0}'.format(e))
    fail = True
except clap.errors.ConflictingOptionsError as e:
    print('conflicting options found: {0}'.format(e))
    fail = True
except clap.errors.RequiredOptionNotFoundError as e:
    print('required option not found: {0}'.format(e))
    fail = True
except clap.errors.InvalidOperandRangeError as e:
    print('invalid number of operands: {0}'.format(e))
    fail = True
except Exception as e:
    fail = True
    raise e
finally:
    if fail: exit()
    else: ui = parser.parse().ui().finalise()


# Setting constants for later use
TARGET = os.path.abspath(ui.get('-t') if '--target' in ui else '.')
print('TARGET:', repr(TARGET))
SITE_PATH = bearton.util.env.getrepopath(TARGET, nofail=True)
print('SITE_PATH:', repr(SITE_PATH))


# Creating widely used objects
msgr = bearton.util.messenger.Messenger(verbosity=(ui.get('-v') if '--verbose' in ui else 0), debugging=('--debug' in ui), quiet=('--quiet' in ui))
db = bearton.db.db(path=SITE_PATH).load()
config = bearton.config.Configuration(path=SITE_PATH).load(guard=True)


# -----------------------------
#   UI logic code goes HERE!  |
# -----------------------------
if '--version' in ui:
    msgr.debug('verbosity level: {0}'.format(ui.get('--verbose') if '--verbose' in ui else 0))
    msgr.message('bearton version {0}'.format(bearton.__version__), 0)
    for name, module in [('clap', clap), ('muspyche', muspyche)]:
        msgr.debug('using "{0}" library v. {1}'.format(name, module.__version__))
if clap.helper.HelpRunner(ui=ui, program=_file).run().displayed(): exit()

if not ui.islast(): ui = ui.down()

# --------------------------------------
#   Per-mode UI logic code goes HERE!  |
# --------------------------------------
if str(ui) == '':
    pass
else:
    try: bearton.util.inrepo(path=TARGET, panic=True)
    except bearton.exceptions.BeartonError as e: msgr.message('fatal: {0}'.format(e))
    finally: pass


# Storing widely used objects state
config.store().unload()
db.store().unload()
