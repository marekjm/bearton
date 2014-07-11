#!/usr/bin/env python3

import json
import os
import shutil
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

# Creating widely used objects
msgr = bearton.util.messenger.Messenger(verbosity=(ui.get('-v') if '--verbose' in ui else 0), debugging=('--debug' in ui), quiet=('--quiet' in ui))


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
msgr.setVerbosity(ui.get('-v') if '--verbose' in ui else 0)
msgr.setDebug('--debug' in ui)

# --------------------------------------
#   Per-mode UI logic code goes HERE!  |
# --------------------------------------
config = bearton.config.Configuration(bearton.util.env.getrepopath(TARGET)).load()
if str(ui) == 'get':
    if len(ui.operands()) > 1:
        msgr.message('fail: invalid number of operands: expected at most 1 but got {0}'.format(len(ui.operands())))
        exit(1)
    if '--list' in ui:
        if '--verbose' in ui: output = dict(config.items())
        else: output = config.keys()
        if '--json' in ui: msgr.message(json.dumps(output), 0)
        else:
            if '--verbose' in ui: output = ['{0}={1}'.format(k, v) for k, v in output.items()]
            for i in output: msgr.message(i, 0)
    elif '--key' in ui:
        output = config.get(ui.get('-k'))
        if '--json' in ui: output = json.dumps(output)
        msgr.message(output, 0)
    elif ui.operands():
        output = config.get(ui.operands()[0])
        if '--json' in ui: output = json.dumps(output)
        msgr.message(output, 0)
elif str(ui) == 'set':
    if len(ui.operands()) > 2:
        msgr.message('fail: invalid number of operands: expected at most 2 but got {0}'.format(len(ui.operands())))
    else:
        key, value = '', ''
        operands = ui.operands()
        if operands: key = operands.pop(0)
        if operands: value = operands.pop(0)
        msgr.debug('{0} -> {1}'.format(key, repr(value)))
        if key: config.set(key, value).store()
elif str(ui) == 'rm':
    for k in ui.operands():
        if '--pop' in ui: msgr.message(config.pop(k), 0)
        else: config.remove(k)
    config.store()
