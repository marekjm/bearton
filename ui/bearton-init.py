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

msgr = bearton.util.Messenger(verbosity=0, debugging=('--debug' in ui))

SITE_PATH = (ui.get('-t') if '--target' in ui else '.')
SCHEMES_PATH = (ui.get('-s') if '--schemes' in ui else os.path.join(SITE_PATH, '.bearton', 'schemes'))

if str(ui) == 'init':
    path = os.path.abspath(SITE_PATH)
    schemes_path = ('' if '--no-schemes' in ui else SCHEMES_PATH)
    if '--force' in ui: bearton.init.rm(path, msgr)
    bearton.init.new(target=path, schemes=schemes_path, msgr=msgr)
    msgr.message('initialized Bearton local in {0}'.format(path), 0)
elif str(ui) == 'rm':
    target = (ui.get('-t') if '--target' in ui else '.')
    target = os.path.abspath(target)
    if '.bearton' in os.listdir(target):
        bearton.init.rm(target, msgr)
        msgr.debug('removed Bearton repository from {0}'.format(target))
    else:
        msgr.debug('no Bearton repository found in {0}'.format(target))
