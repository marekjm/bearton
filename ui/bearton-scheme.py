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
TARGET = os.path.abspath(ui.get('-t') if '--target' in ui else '.')
SITE_PATH = bearton.util.getrepopath(TARGET)
SCHEMES_PATH = (ui.get('-S') if '--schemes' in ui else bearton.util.getschemespath(cwd=SITE_PATH))


# Creating widely used objects
msgr = bearton.util.Messenger(verbosity=int('--verbose' in ui), debugging=('--debug' in ui), quiet=('--quiet' in ui))
db = bearton.db.db(path=SITE_PATH).load()
config = bearton.config.Configuration(path=SITE_PATH).load(guard=True)


if bearton.util.inrepo(path=TARGET) and str(ui) == 'apply':
    name = ''
    if 'scheme' in config: name = config.get('scheme')
    if ui.arguments: name= ui.arguments[0]
    if '--name' in ui: name = ui.get('-n')

    if name:
        msgr.debug('defined name of the scheme: {0}'.format(name))
    if not name:
        msgr.message('fatal: cannot define name of the scheme to apply')
        exit(1)
    if name not in os.listdir(SCHEMES_PATH):
        msgr.message('fatal: coud not find scheme "{0}" in {1}'.format(name, SCHEMES_PATH))
        if '--schemes' not in ui: msgr.message('note: try setting different schemes location with -S/--schemes option')
        exit(1)

    if '--force' in ui: bearton.schemes.loader.rm(os.path.join(SCHEMES_PATH, name), SITE_PATH, msgr)
    bearton.schemes.loader.apply(os.path.join(SCHEMES_PATH, name), SITE_PATH, msgr)
elif bearton.util.inrepo(path=TARGET) and str(ui) == 'rm':
    name = (config.get('scheme') if 'scheme' in config else '')
    if not name:
        msgr.message('fatal: cannot define name of the scheme to remove')
        exit(1)
    bearton.schemes.loader.rm(os.path.join(SCHEMES_PATH, name), SITE_PATH, msgr)
elif bearton.util.inrepo(path=TARGET) and str(ui) == 'inspect':
    name = (config.get('scheme') if 'scheme' in config else '')
    if not name:
        msgr.message('fatal: cannot define name of the scheme to remove')
        exit(1)
    if '--elements' in ui:
        els = bearton.schemes.inspector.getElementMetas(name)
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
        output = str([name for name, meta in els])
        msgr.message(output, 0)
elif str(ui) == '':
    if '--version' in ui: msgr.message(('bearton version {0}' if '--verbose' in ui else '{0}').format(bearton.__version__), 0)
    if '--help' in ui:
        print('\n'.join(clap.helper.Helper(ui).help()))
else:
    try: bearton.util.inrepo(path=TARGET, panic=True)
    except bearton.exceptions.BeartonError as e: msgr.message('fatal: {0}'.format(e))
    finally: pass


# Storing widely used objects state
config.store().unload()
db.store().unload()
