#!/usr/bin/env python3

import json
import os
from sys import argv

import clap
import muspyche

import bearton


# Building UI
argv = list(clap.formatter.Formatter(argv[1:]).format())
_file = os.path.splitext(os.path.split(__file__)[-1])[0]
uipath = os.path.join(bearton.util.getuipath(), '{0}.clap.json'.format(_file))

try:
    ifstream = open(uipath, 'r')
    model = json.loads(ifstream.read())
    ifstream.close()
    err = None
except Exception as e:
    err = e
finally:
    if err is not None:
        print('failed to read UI description conatined in "{0}": {1}'.format(uipath, err))
        exit(1)

mode = clap.builder.Builder(model).build().get()
parser = clap.parser.Parser(mode).feed(argv)

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
SITE_PATH = bearton.util.getrepopath(TARGET)
SCHEMES_PATH = (ui.get('-S') if '--schemes' in ui else bearton.util.getschemespath(cwd=SITE_PATH))


# Creating widely used objects
msgr = bearton.util.Messenger(verbosity=(ui.get('-v') if '--verbose' in ui else 0), debugging=('--debug' in ui), quiet=('--quiet' in ui))
db = bearton.db.db(path=SITE_PATH).load()
config = bearton.config.Configuration(path=SITE_PATH).load(guard=True)


# -----------------------------
#   UI logic code goes HERE!  |
# -----------------------------
# ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓
if str(ui) == '':
    if '--version' in ui:
        msgr.debug('verbosity level: {0}'.format(ui.get('--verbose') if '--verbose' in ui else 0))
        msgr.message('bearton version {0}'.format(bearton.__version__), 0)
        for name, module in [('clap', clap), ('muspyche', muspyche), ('clap', clap)]:
            msgr.debug('using "{0}" library v. {1}'.format(name, module.__version__))

hui = ui
while True:
    if '--help' in hui:
        helper = clap.helper.Helper(_file, hui._mode).setmaxlen(n=140)
        usage = []
        if hui.up() is hui: [helper.addUsage(i) for i in usage]
        msgr.message(helper.gen(deep=('--verbose' in hui)).render())
        if '--verbose' not in hui: msgr.message('\nRun "{0} --help --verbose" to see full help message'.format(_file))
        exit(0)
    if hui.islast(): break
    hui = hui.down()

if not ui.islast(): ui = ui.down()

# --------------------------------------
#   Per-mode UI logic code goes HERE!  |
# --------------------------------------
# ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓
if str(ui) == '':
    pass
else:
    try: bearton.util.inrepo(path=TARGET, panic=True)
    except bearton.exceptions.BeartonError as e: msgr.message('fatal: {0}'.format(e))
    finally: pass


# Storing widely used objects state
config.store().unload()
db.store().unload()
