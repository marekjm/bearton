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
if bearton.util.inrepo(path=TARGET) and str(ui) == 'query':
    if '--raw' in ui:
        scheme, element, queryd, querytags = db._parsequery(ui.get('-r'))
    else:
        if len(ui.operands()) > 2:
            msgr.message('fatal: invalid number of operands: expected at most 2 but got {0}'.format(len(ui.operands())))
            exit(1)
        scheme = (ui.operands().pop(0) if len(ui.operands()) == 2 else config.get('scheme'))
        scheme = (ui.get('-s') if '--scheme' in ui else scheme)
        element = (ui.operands().pop(0) if ui.operands() else '')
        element = (ui.get('-e') if '--element' in ui else element)
        queryd = {}
        for a in ui.operands():
            if '=' not in a: continue
            a = a.split('=', 1)
            key, value = a[0], a[1]
            queryd[key] = value
        querytags = (ui.get('--tags').split(',') if '--tags' in ui else [])
    msgr.debug('query: scheme={0}, element={1}, queryd={2}, querytags={3}'.format(scheme, element, queryd, querytags))
    pages = (bearton.db.db(path=SITE_PATH, base=True).load() if '--base' in ui else db).query(scheme, element, queryd, querytags)
    pages = [key for key, entry in pages]
    if '--verbose' in ui: signature = ('{:key@}: {:name@meta}@{:scheme@meta}' if '--format' not in ui else ui.get('-F'))
    else: signature = '{:key@}'
    if '--with-output' in ui: signature += ' {:output@meta}'
    for i in pages: msgr.message(db.get(i).getsignature(signature), 0)
elif bearton.util.inrepo(path=TARGET) and str(ui) == 'update':
    if '--erase' in ui:
        really = ('yes' if '--yes' in ui else input('do you really want to wipe out the database? [y/n] '))
        really = (True if really.strip().lower() in ['y', 'yes'] else False)
        if not really:
            msgr.debug('cancelled database wipeout')
        else:
            db.erase()
            msgr.debug('wiped database contents from: {0}'.format(os.path.join(SITE_PATH, '.bearton', 'db')))
    else:
        metadata, contexts = db.update(SCHEMES_PATH)
        for name, value in [('metadata', metadata), ('context', contexts)]:
            if value: msgr.message('number of db entries with update to: {0}: {1}'.format(name, len(value)), 0)
        if contexts:
            log = os.path.join('.', 'bearton.required_context_edits.log')
            if '--context-edits-log' in ui: log = ui.get('--context-edits-log')
            bearton.util.writefile(log, '\n'.join(contexts))
            msgr.message('entries that possibly - in case something was added - require context edits were placed in "{0}" file'.format(log), 0)
