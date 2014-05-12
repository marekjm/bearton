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
config = bearton.config.Configuration(path=SITE_PATH).load()


if str(ui) == 'init':
    path = os.path.abspath(SITE_PATH)
    if '--clean' in ui:
        msgr.debug('cleaning')
        bearton.init.rm(path, msgr)
    if '--no-write' not in ui:
        if '--update' in ui:
            bearton.init.update(target=path, msgr=msgr)
        else:
            bearton.init.new(target=path, schemes=SCHEMES_PATH, msgr=msgr)
        db.load()
        config.load()
        msgr.message('{0} Bearton local in {1}'.format(('updated' if '--update' in ui else 'initialized'), path), 1)
    if '--clean' in ui and '--no-write' in ui: #equivalent to removal
        db.unload()
        config.unload()
elif str(ui) == 'rm':
    target = (ui.get('-t') if '--target' in ui else '.')
    target = os.path.abspath(target)
    if '.bearton' in os.listdir(target):
        bearton.init.rm(target, msgr)
        msgr.debug('removed Bearton repository from {0}'.format(target))
    else:
        msgr.debug('no Bearton repository found in {0}'.format(target))
    exit() # to prevent config and db from being stored
elif bearton.util.inrepo(path=TARGET) and str(ui) == 'sync':
    print('ui mode:', ui.mode)
    print('ui arguments:', ui.arguments)
    print('ui parsed:', ui.parsed)
    if '--schemes' in ui:
        msgr.message(SCHEMES_PATH, 0)
        current_schemes_path = os.path.join(SITE_PATH, '.bearton', 'schemes')
        current_schemes = os.listdir(current_schemes_path)
        available_schemes = os.listdir(SCHEMES_PATH)
        to_update = (available_schemes if '--all' in ui else [s for s in available_schemes if s in current_schemes])
        msgr.debug('current schemes: {0}'.format(', '.join(current_schemes)))
        msgr.debug('available schemes: {0}'.format(', '.join(available_schemes)))
        msgr.message('schemes to update: {0}'.format(', '.join(to_update)), 0)
        bearton.init.syncschemes(target=current_schemes_path, schemes=SCHEMES_PATH, wanted=to_update, msgr=msgr)
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
