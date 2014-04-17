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
SCHEMES_PATH = (ui.get('-S') if '--schemes-path' in ui else bearton.util.getschemespath(cwd=SITE_PATH))


# Creating widely used objects
msgr = bearton.util.Messenger(verbosity=0, debugging=('--debug' in ui), quiet=('--quiet' in ui))
db = bearton.db.Database(path=SITE_PATH).load()
config = bearton.config.Configuration(path=SITE_PATH).load(guard=True)


if str(ui) == 'new':
    # Obtaining scheme and element
    scheme = (config.get('scheme') if 'scheme' in config else 'default')
    scheme = (ui.arguments.pop(0) if len(ui.arguments) > 1 else 'default')
    element = (ui.arguments.pop(0) if ui.arguments else '')
    if '--scheme' in ui: scheme = ui.get('-s')
    if '--element' in ui: element = ui.get('-e')

    if not element:
        msgr.debug('cannot define what element to use')
        msgr.message('fatal: element required', 0)
        exit(1)

    # Performing necessary checks
    element_meta = os.path.join(SCHEMES_PATH, scheme, 'elements', element, 'meta.json')
    if not os.path.isfile(element_meta):
        msgr.message('fatal: cannot find metadata for element {0} in scheme {1}'.format(element, scheme))
        exit(1)
    element_meta = json.loads(bearton.util.readfile(element_meta))
    if '--base' in ui:
        if element_meta['base'] == False or 'base' not in element_meta:
            msgr.message('fatal: cannot add page as a base element', 0)
            exit(1)
    if '--base' in ui and element in os.listdir(os.path.join(SITE_DB_PATH, 'base')):
        msgr.message('fatal: base element \'{0}\' already created: try \'bearton page edit -bp {0}\' command'.format(element), 0)
        exit(1)
    if 'singular' in element_meta:
        if element_meta['singular'] and len(db.query(scheme, element)) > 0:
            msgr.message('failed to create element {0}: element is singular'.format(element), 0)
            exit(1)

    # Debugging info
    msgr.debug('using scheme path: {0}'.format(SCHEMES_PATH))
    msgr.debug('using scheme: {0}'.format(scheme))
    msgr.debug('using element: {0}'.format(element))
    msgr.debug('target directory: {0}'.format(SITE_PATH))

    # Actual call creating new page in database
    creator = (bearton.page.page.newbase if '--base' in ui else bearton.page.page.new)
    hashed = creator(path=SITE_PATH, schemes_path=SCHEMES_PATH, scheme=scheme, element=element, msgr=msgr)
    # Editing?
    if '--edit' in ui: bearton.page.page.edit(path=SITE_PATH, page=hashed, msgr=msgr)
    # Final message
    msgr.message('created new page: {0}'.format(hashed), 0)
elif str(ui) == 'edit':
    page_id = ''
    if ui.arguments: page_id = ui.arguments[0]
    if '--page-id' in ui: page_id = ui.get('-p')
    if not page_id:
        msgr.message('fail: page id is required')
        exit(1)
    msgr.message('editing page {0}'.format(page_id))
elif str(ui) == 'build':
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


# Storing widely used objects state
config.store().unload()
db.store().unload()
