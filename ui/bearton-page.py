import json
import os
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
SCHEMES_PATH = (ui.get('-S') if '--schemes-path' in ui else '/usr/share/bearton/schemes')

db = bearton.db.Database(path=SITE_PATH).load()

if str(ui) == 'new':
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
    element_meta = json.loads(bearton.util.readfile(os.path.join(SCHEMES_PATH, scheme, 'elements', element, 'meta.json')))
    if 'singular' in element_meta:
        if element_meta['singular'] and len(db.query({'scheme': scheme, 'name': element})) > 0:
            msgr.message('failed to create element {0}: element is singular'.format(element), 0)
            exit(1)
    hashed = bearton.page.page.new(path=SITE_PATH, schemes_path=SCHEMES_PATH, scheme='default', element='home', msgr=msgr)
    entry = bearton.db.Entry(SITE_DB_PATH, hashed).load()
    if 'scheme' not in entry._meta: entry.setinmeta('scheme', scheme)
    if 'name' not in entry._meta: entry.setinmeta('name', element)
    entry.store()
    if '--edit' in ui: bearton.page.page.edit(path=SITE_PATH, page=hashed, msgr=msgr)
    msgr.message('created new page: {0}'.format(hashed), 0)
elif str(ui) == 'query':
    if '--list' in ui:
        pages = db.keys()
        for i in pages:
            msg = i
            msgr.message(msg)
    else:
        queryd = {}
        if '--scheme' in ui: queryd['scheme'] = ui.get('-s')
        if '--element' in ui: queryd['name'] = ui.get('-e')
        for a in ui.arguments:
            if '=' not in a: continue
            a = a.split('=', 1)
            key, value = a[0], a[1]
            queryd[key] = value
        msgr.debug('query: {0}'.format(queryd))
        pool = db.query(queryd)
        for key, entry in pool:
            msgr.message(key, 0)
elif str(ui) == 'edit':
    page_id = ''
    if ui.arguments: page_id = ui.arguments[0]
    if '--page-id' in ui: page_id = ui.get('-p')
    if not page_id:
        msgr.message('fail: page id is required')
        exit(1)
    msgr.message('editing page {0}'.format(page_id))
elif str(ui) == 'build':
    db = bearton.db.Database(path=SITE_PATH).load()
    pages = (db.keys() if '--all' in ui else [i for i in ui.arguments])
    for page in pages:
        msgr.message('building page: {0}'.format(page), 0)
        bearton.page.builder.build(path=SITE_PATH, schemes=SCHEMES_PATH, page=page, msgr=msgr)
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
            db.wipe()
            msgr.debug('wiped database contents from: {0}'.format(SITE_DB_PATH))

db.store().unload()
