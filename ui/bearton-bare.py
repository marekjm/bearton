#!/usr/bin/env python3

import json
import os
from sys import argv

import clap
import muspyche

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
# if --verbose is used, msgr has a verbosity level 1; else it is 0
msgr = bearton.util.Messenger(verbosity=int('--verbose' in ui), debugging=('--debug' in ui), quiet=('--quiet' in ui))
db = bearton.db.db(path=SITE_PATH).load()
config = bearton.config.Configuration(path=SITE_PATH).load(guard=True)


# -----------------------------
#   UI logic code goes HERE!  |
# -----------------------------
if str(ui) == '':
    if '--version' in ui:
        msgr.message(('bearton version {0}' if '--verbose' in ui else '{0}').format(bearton.__version__), 0)
        for name, module in [('clap', clap), ('muspyche', muspyche)]:
            msgr.debug('using "{0}" library v. {1}'.format(name, module.__version__))
    if '--help' in ui:
        print('\n'.join(clap.helper.Helper(ui).help()))


# Storing widely used objects state
config.store().unload()
db.store().unload()
