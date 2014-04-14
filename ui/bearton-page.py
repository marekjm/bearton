import json
import os
import shutil
from sys import argv

import clap

import bearton


args = clap.formater.Formater(argv[1:])
args.format()

builder = clap.builder.Builder('./ui/bearton-page.json', argv=list(args))
builder.build()

ui = builder.get()
ui.check()
ui.parse()

msgr = bearton.util.Messenger(verbosity=0, debugging=('--debug' in ui), quiet=('--quiet' in ui))

SITE_PATH = (ui.get('-w') if '--where' in ui else '.')
SITE_DB_PATH = os.path.join(SITE_PATH, '.bearton', 'db')

if str(ui) == 'new':
    SCHEMES_PATH = '/usr/share/bearton/schemes'

    if '--schemes-path' in ui: SCHEMES_PATH = ui.get('-S')

    scheme = (ui.arguments.pop(0) if len(ui.arguments) > 1 else 'default')
    element = (ui.arguments.pop(0) if ui.arguments else '')

    if '--scheme' in ui: scheme = ui.get('-s')
    if '--element' in ui: element = ui.get('-e')

    if not element:
        msgr.debug('cannot define what element to use')
        msgr.message('fatal: element required', 0)
        exit(1)

    msgr.debug('using scheme path: {0}'.format(SCHEMES_PATH))
    msgr.debug('using scheme: {0}'.format(scheme))
    msgr.debug('using element: {0}'.format(element))
    msgr.debug('target directory: {0}'.format(SITE_PATH))
    hashed = bearton.page.new(path=SITE_PATH, schemes_path=SCHEMES_PATH, scheme='default', element='home', msgr=msgr)
    if '--edit' in ui: bearton.page.edit(path=SITE_PATH, page=hashed, msgr=msgr)
    msgr.message('created new page: {0}'.format(hashed), 0)
elif str(ui) == 'query':
    if '--list' in ui:
        pages = os.listdir(SITE_DB_PATH)
        for i in pages: msgr.message(i)
elif str(ui) == 'edit':
    page_id = ''
    if ui.arguments: page_id = ui.arguments[0]
    if '--page-id' in ui: page_id = ui.get('-p')
    if not page_id:
        msgr.message('fail: page id is required')
        exit(1)
    msgr.message('editing page {0}'.format(page_id))
elif str(ui) == 'build':
    pages = (os.listdir(SITE_DB_PATH) if '--all' in ui else [i for i in ui.arguments])
    for page in pages:
        msgr.message('building page: {0}'.format(page), 0)
elif str(ui) == 'rm':
    page_id = ''
    if ui.arguments: page_id = ui.arguments[0]
    if '--page-id' in ui: page_id = ui.get('-p')
    if not page_id:
        msgr.message('fail: page id is required')
        exit(1)
    msgr.message('removing page {0}'.format(page_id))
else:
    if '--wipe-db' in ui:
        really = ('yes' if '--yes' in ui else input('do you really want to wipe out the database? [y/n] '))
        really = (True if really.strip().lower() in ['y', 'yes'] else False)
        if not really:
            msgr.debug('cancelled database wipeout')
        else:
            shutil.rmtree(SITE_DB_PATH)
            msgr.debug('wiped database contents from: {0}'.format(SITE_DB_PATH))
            os.mkdir(SITE_DB_PATH)
