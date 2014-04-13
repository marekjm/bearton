import json
import os
from sys import argv

import clap

import bearton


args = clap.formater.Formater(argv[1:])
args.format()

builder = clap.builder.Builder('./ui/bearton-config.json', argv=list(args))
builder.build()

ui = builder.get()
ui.check()
ui.parse()

msgr = bearton.util.Messenger(verbosity=0)

config = bearton.config.Configuration(path=(ui.get('-w') if '--where' in ui else '.'))
if str(ui) != '': config.load()

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

if str(ui) != '': config.store()
