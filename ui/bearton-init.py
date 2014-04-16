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

msgr = bearton.util.Messenger(verbosity=0, debugging=('--debug' in ui), quiet=('--quiet' in ui))

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
elif str(ui) == 'sync':
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
