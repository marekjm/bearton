import json
import os
from sys import argv

import clap

import bearton


args = clap.formater.Formater(argv[1:])
args.format()

builder = clap.builder.Builder('./ui/bearton-db.json', argv=list(args))
builder.build()

ui = builder.get()
ui.check()
ui.parse()

msgr = bearton.util.Messenger(verbosity=0, debugging=('--debug' in ui), quiet=('--quiet' in ui))

SITE_PATH = (ui.get('-t') if '--target' in ui else '.')
SITE_DB_PATH = os.path.join(SITE_PATH, '.bearton', 'db')
SCHEMES_PATH = (ui.get('-S') if '--schemes-path' in ui else os.path.join(SITE_PATH, '.bearton', 'schemes'))

db = bearton.db.Database(path=SITE_PATH).load()
config = bearton.config.Configuration(path=SITE_PATH).load()

if str(ui) == 'query':
    if '--list' in ui:
        pages = db.keys()
        for i in pages:
            msg = i
            msgr.message(msg)
    else:
        queryd = {}
        scheme = (ui.get('-s') if '--scheme' in ui else '')
        element = (ui.get('-e') if '--element' in ui else '')
        for a in ui.arguments:
            if '=' not in a: continue
            a = a.split('=', 1)
            key, value = a[0], a[1]
            queryd[key] = value
        msgr.debug('query: scheme={0}, element={1}, queryd={2}'.format(scheme, element, queryd))
        pool = db.query(scheme, element, queryd)
        for key, entry in pool:
            msgr.message(key, 0)
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
            if value: msgr.message('number of db entries with update to: {0}: {0}'.format(name, len(value)), 0)
        if contexts:
            log = os.path.join('.', 'bearton.required_context_edits.log')
            if '--context-edits-log' in ui: log = ui.get('--context-edits-log')
            bearton.util.writefile(log, '\n'.join(contexts))
            msgr.message('entries that possibly - in case something was added - require context edits were placed in "{0}" file'.format(log), 0)

db.store().unload()
