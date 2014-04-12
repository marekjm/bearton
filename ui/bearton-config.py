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
                for k, v in output.items(): tmp.append('{0} = {1}'.format(k, v))
                output = tmp
            for i in output:
                msgr.message(i, 0)

if str(ui) != '': config.store()
