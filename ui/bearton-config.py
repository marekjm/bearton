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


if bearton.util.inrepo(path=TARGET) and str(ui) == 'get':
    if len(ui.arguments) > 1:
        msgr.message('fail: invalid number of operands: expected at most 1 but got {0}'.format(len(ui.arguments)))
        exit(1)
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
elif bearton.util.inrepo(path=TARGET) and str(ui) == 'set':
    if len(ui.arguments) > 2:
        msgr.message('fail: invalid number of operands: expected at most 2 but got {0}'.format(len(ui.arguments)))
    else:
        key, value = '', ''
        if ui.arguments: key = ui.arguments.pop(0)
        if ui.arguments: value = ui.arguments.pop(0)
        if '--key' in ui: key = ui.get('-k')
        if '--value' in ui: value = ui.get('-v')
        msgr.debug('{0} -> {1}'.format(key, value))
        if key: config.unguard().set(key, value).guard()
elif bearton.util.inrepo(path=TARGET) and str(ui) == 'rm':
    keys = [k for k in ui.arguments]
    if '--key' in ui: keys = [ui.get('-k')]
    config.unguard()
    if '--pop' in ui:
        msgr.message(config.pop(keys[0]), 0)
    else:
        for k in keys: config.remove(k)
    config.guard()
elif str(ui) == '':
    if '--version' in ui: msgr.message(('bearton version {0}' if '--verbose' in ui else '{0}').format(bearton.__version__), 0)
    if '--help' in ui:
        msgr.message('\n'.join(clap.helper.Helper(ui).help()))


# Storing widely used objects state
config.store().unload()
db.store().unload()
