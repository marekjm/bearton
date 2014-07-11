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
if str(ui) == 'apply':
    cnfg = bearton.config.Configuration(bearton.util.env.getrepopath(TARGET)).load()
    name = ''
    if 'scheme' in cnfg: name = cnfg.get('scheme')
    if ui.operands(): name= ui.operands()[0]
    if not name:
        msgr.message('fatal: cannot define name of the scheme to apply')
        exit(1)
    if name not in [schm for schm, path in bearton.util.env.listschemes(bearton.util.env.getschemespaths(TARGET))]:
        msgr.message('fatal: coud not find scheme "{0}"'.format(name))
        exit(1)
    if name: msgr.debug('defined name of the scheme: {0}'.format(name))
    source = ''
    for schm, path in bearton.util.env.listschemes(bearton.util.env.getschemespaths(TARGET)):
        if schm == name:
            source = os.path.join(path, schm)
            break
    bearton.schemes.loader.apply(source, TARGET, msgr)
elif str(ui) == 'inspect':
    cnfg = bearton.config.Configuration(bearton.util.env.getrepopath(TARGET)).load()
    name = (cnfg.get('scheme') if 'scheme' in cnfg else '')
    if ui.operands(): name = ui.operands()[0]
    if not name:
        msgr.message('fatal: cannot define name of the scheme to inspect')
        exit(1)
    if name not in [schm for schm, path in bearton.util.env.listschemes(bearton.util.env.getschemespaths(TARGET))]:
        msgr.message('fatal: coud not find scheme "{0}"'.format(name))
        exit(1)
    path = os.path.join([path for schm, path in bearton.util.env.listschemes(bearton.util.env.getschemespaths(TARGET)) if schm == name][0], name)
    msgr.debug('defined name of the scheme: {0}'.format(name))
    msgr.debug('defined path of the scheme: {0}'.format(path))
    if '--elements' in ui:
        els = bearton.schemes.inspector.getElementMetas(path)
        if '--base' in ui:
            f = []
            for name, meta in els:
                if 'base' in meta and meta['base']: f.append( (name, meta) )
            if '--not' in ui: f = [i for i in els if i not in f]
            els = f[:]
        elif '--buildable' in ui:
            f = []
            for name, meta in els:
                ok = 0
                if 'output' in meta and meta['output'] != '': ok += 1
                if 'base' not in meta or not meta['base']: ok += 1
                if ok == 2: f.append( (name, meta) )
            if '--not' in ui: f = [i for i in els if i not in f]
            els = f[:]
        for i in sorted([name for name, meta in els]): msgr.message(i)
elif str(ui) == 'ls':
    """Mode used to list available schemes.
    """
    cnfg = bearton.config.Configuration(bearton.util.env.getrepopath(TARGET)).load()
    scheme_paths = bearton.util.env.getschemespaths(TARGET)
    schemes = bearton.util.env.listschemes(scheme_paths)
    if '--group' in ui:
        groups = {}
        for schm, path in schemes:
            if path not in groups: groups[path] = []
            groups[path].append(schm)
        for path in sorted(groups.keys()):
            msgr.message('  {0}'.format(path))
            for schm in sorted(groups[path]): msgr.message('   {1} {0}'.format(schm, ('+' if (schm == cnfg.get('scheme') and '--mark-current' in ui) else ' ')))
    else:
        for schm, path in schemes:
            msg = ' {1} {0}'.format(schm, ('+' if (schm == cnfg.get('scheme') and '--mark-current' in ui) else ' '))
            if '--verbose' in ui: msg = '{0} :: {1}'.format(msg, path)
            msgr.message(msg)
