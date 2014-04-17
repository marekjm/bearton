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
SCHEMES_PATH = (ui.get('-S') if '--schemes-path' in ui else os.path.join(SITE_PATH, '.bearton', 'schemes'))


# Creating widely used objects
msgr = bearton.util.Messenger(verbosity=0, debugging=('--debug' in ui), quiet=('--quiet' in ui))
db = bearton.db.Database(path=SITE_PATH).load()
config = bearton.config.Configuration(path=SITE_PATH).load()


if str(ui) == 'get':
    if '--list' in ui:
        if '--verbose' in ui:
            output = dict(config.kvalues())
        else:
            output = config.keys()
        if '--json' in ui:
            output = json.dumps(output)
            msgr.message(output, 0)
        else:
            if '--verbose' in ui:
                tmp = []
                for k, v in output.items(): tmp.append('{0}={1}'.format(k, v))
                output = tmp
            for i in output:
                msgr.message(i, 0)
    elif '--key' in ui:
        output = config.get(ui.get('-k'))
        if '--json' in ui: output = json.dumps(output)
        msgr.message(output, 0)
    elif ui.arguments:
        output = config.get(ui.arguments[0])
        if '--json' in ui: output = json.dumps(output)
        msgr.message(output, 0)
elif str(ui) == 'set':
    key, value = '', ''
    if ui.arguments: key = ui.arguments.pop(0)
    if ui.arguments: value = ui.arguments.pop(0)
    if '--key' in ui: key = ui.get('-k')
    if '--value' in ui: value = ui.get('-v')
    msgr.debug('{0} -> {1}'.format(key, value))
    config.set(key, value)
elif str(ui) == 'rm':
    keys = []
    if ui.arguments: keys = [k for k in ui.arguments]
    if '--key' in ui: keys = [ui.get('-k')]
    if '--pop' in ui:
        msgr.message(config.pop(keys[0]), 0)
    else:
        for k in keys: config.remove(k)


# Storing widely used objects state
config.store().unload()
db.store().unload()
