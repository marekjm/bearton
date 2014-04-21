#!/usr/bin/env python3

import json
import os
from sys import argv

import clap

import bearton


# Building UI
args = clap.formater.Formater(argv[1:])
args.format()

_file = os.path.splitext(os.path.split(__file__)[-1])[0]
uipath = os.path.join(bearton.util.getuipath(), '{0}.json'.format(_file))
builder = clap.builder.Builder(uipath, argv=list(args))
builder.build()

ui = builder.get()
ui.check()
ui.parse()


# Setting constants for later use
SITE_PATH = (ui.get('-t') if '--target' in ui else '.')
SITE_DB_PATH = os.path.join(SITE_PATH, '.bearton', 'db')
SCHEMES_PATH = (ui.get('-S') if '--schemes' in ui else bearton.util.getschemespath(cwd=SITE_PATH))


# Creating widely used objects
msgr = bearton.util.Messenger(verbosity=int('--verbose' in ui), debugging=('--debug' in ui), quiet=('--quiet' in ui))
db = bearton.db.db(path=SITE_PATH).load()
config = bearton.config.Configuration(path=SITE_PATH).load(guard=True)


if str(ui) == 'query':
    if '--raw' in ui:
        scheme, element, queryd, querytags = db._parsequery(ui.get('-r'))
    else:
        if len(ui.arguments) > 2:
            msgr.message('fatal: invalid number of operands: expected at most 2 but got {0}'.format(len(ui.arguments)))
            exit(1)
        scheme = (ui.arguments.pop(0) if len(ui.arguments) == 2 else config.get('scheme'))
        scheme = (ui.get('-s') if '--scheme' in ui else scheme)
        element = (ui.arguments.pop(0) if ui.arguments else '')
        element = (ui.get('-e') if '--element' in ui else element)
        queryd = {}
        for a in ui.arguments:
            if '=' not in a: continue
            a = a.split('=', 1)
            key, value = a[0], a[1]
            queryd[key] = value
        querytags = (ui.get('--tags').split(',') if '--tags' in ui else [])
    msgr.debug('query: scheme={0}, element={1}, queryd={2}, querytags={3}'.format(scheme, element, queryd, querytags))
    pages = (bearton.db.db(path=SITE_PATH, base=True).load() if '--base' in ui else db).query(scheme, element, queryd, querytags)
    pages = [key for key, entry in pages]
    for i in pages:
        if '--verbose' in ui:
            msg = db.get(i).getsignature(('{:key@}: {:name@meta}@{:scheme@meta}' if '--format' not in ui else ui.get('-F')))
        else:
            msg = i
        msgr.message(msg, 0)
elif str(ui) == 'update':
    if '--wipe' in ui:
        really = ('yes' if '--yes' in ui else input('do you really want to wipe out the database? [y/n] '))
        really = (True if really.strip().lower() in ['y', 'yes'] else False)
        if not really:
            msgr.debug('cancelled database wipeout')
        else:
            db.wipe()
            msgr.debug('wiped database contents from: {0}'.format(SITE_DB_PATH))
    else:
        metadata, contexts = db.update(SCHEMES_PATH)
        for name, value in [('metadata', metadata), ('context', contexts)]:
            if value: msgr.message('number of db entries with update to: {0}: {1}'.format(name, len(value)), 0)
        if contexts:
            log = os.path.join('.', 'bearton.required_context_edits.log')
            if '--context-edits-log' in ui: log = ui.get('--context-edits-log')
            bearton.util.writefile(log, '\n'.join(contexts))
            msgr.message('entries that possibly - in case something was added - require context edits were placed in "{0}" file'.format(log), 0)


# Storing widely used objects state
config.store().unload()
db.store().unload()
