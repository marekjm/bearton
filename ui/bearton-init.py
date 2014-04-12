import json
import os
from sys import argv

import clap

import bearton


args = clap.formater.Formater(argv[1:])
args.format()

builder = clap.builder.Builder('./ui/bearton-init.json', argv=list(args))
builder.build()

ui = builder.get()
ui.check()
ui.parse()

msgr = bearton.util.Messenger(verbosity=0)

SCHEMES_PATH = '/usr/share/bearton/schemes'

if str(ui) == 'init':
    if '--where' in ui:
        path = ui.get('-w')
    else:
        path = '.'
    path = os.path.abspath(path)
    schemes_path = (ui.get('-s') if '--schemes' in ui else SCHEMES_PATH)
    msgr.message('generating Bearton local in {0}'.format(path), 0)
    if '--force' in ui: bearton.init.rm(path)
    bearton.init.new(where=path, schemes=schemes_path, msgr=msgr)
