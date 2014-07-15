#!/usr/bin/env python3

import json
import os
import shutil
from sys import argv

import clap
import muspyche

import bearton


# Obtaining requred filename and model
_file = os.path.splitext(os.path.split(__file__)[1])[0]
model = bearton.util.env.getuimodel(_file)

# Building UI
argv = list(clap.formatter.Formatter(argv[1:]).format())
command = clap.builder.Builder(model).insertHelpCommand().build().get()
parser = clap.parser.Parser(command).feed(argv)

try:
    clap.checker.RedChecker(parser).check()
    fail = False
except clap.errors.MissingArgumentError as e:
    print('missing argument for option: {0}'.format(e))
    fail = True
except clap.errors.UnrecognizedOptionError as e:
    print('unrecognized option found: {0}'.format(e))
    fail = True
except clap.errors.ConflictingOptionsError as e:
    print('conflicting options found: {0}'.format(e))
    fail = True
except clap.errors.RequiredOptionNotFoundError as e:
    print('required option not found: {0}'.format(e))
    fail = True
except clap.errors.InvalidOperandRangeError as e:
    print('invalid number of operands: {0}'.format(e))
    fail = True
except Exception as e:
    fail = True
    raise e
finally:
    if fail: exit()
    else: ui = parser.parse().ui().finalise()


# Setting constants for later use
TARGET = os.path.abspath(ui.get('-t') if '--target' in ui else '.')

# Creating widely used objects
msgr = bearton.util.messenger.Messenger(verbosity=(ui.get('-v') if '--verbose' in ui else 0), debugging=('--debug' in ui), quiet=('--quiet' in ui))


# -----------------------------
#   UI logic code goes HERE!  |
# -----------------------------
if '--version' in ui:
    msgr.debug('verbosity level: {0}'.format(ui.get('--verbose') if '--verbose' in ui else 0))
    msgr.message('bearton version {0}'.format(bearton.__version__), 0)
    for name, module in [('clap', clap), ('muspyche', muspyche)]:
        msgr.debug('using "{0}" library v. {1}'.format(name, module.__version__))
if clap.helper.HelpRunner(ui=ui, program=_file).run().displayed(): exit()

if not ui.islast(): ui = ui.down()
msgr.setVerbosity(ui.get('-v') if '--verbose' in ui else 0)
msgr.setDebug('--debug' in ui)

msgr.debug('target directory: {0}'.format(bearton.util.env.getrepopath(TARGET)))

# --------------------------------------
#   Per-mode UI logic code goes HERE!  |
# --------------------------------------
if str(ui) == 'new':
    """This mode is employed for creating new pages.
    """
    config = bearton.config.Configuration(bearton.util.env.getrepopath(TARGET)).load()
    db = bearton.db.db(path=bearton.util.env.getrepopath(TARGET)).load()
    # Obtaining scheme and element
    opers = ui.operands()
    scheme = (config.get('scheme') if 'scheme' in config else 'default')
    scheme = (opers.pop(0) if len(opers) == 2 else scheme)
    element = opers.pop(0)

    # Report requested set of scheme:element
    msgr.debug('requested element: "{0}"'.format(element))
    msgr.debug('requested scheme:  "{0}"{1}'.format(scheme, ('' if len(ui.operands()) == 2 else ' (loaded from config)')))

    # Check if scheme can be found and used
    schemes = bearton.util.env.listschemes(bearton.util.env.getschemespaths(TARGET))
    scheme_path = ''
    for schm, path in schemes:
        if schm == scheme:
            scheme_path = path
            break
    if not scheme_path:
        msgr.message('fatal: scheme "{0}" have not been found'.format(scheme))
        exit(1)
    msgr.debug('using scheme "{0}" from "{1}"'.format(scheme, scheme_path))

    # Obtain list of elements available in scheme
    elements = bearton.schemes.inspector.lselements(path=scheme_path, scheme=scheme)
    msgr.debug('available elements: {0}'.format(', '.join(sorted(elements))))

    # Set final element to use
    if element not in elements:
        part, element = element[:], ''
        # Try to find appropriate element for string supplied, e.g. yield `article` for supplied `art`
        candidates = []
        for i in elements:
            if i.startswith(part): candidates.append(i)
        if len(candidates) > 1:
            msgr.debug('"{0}" is ambiguous: resolves to more than one element: {1}'.format(part, ', '.join(candidates)))
        elif len(candidates) < 1:
            msgr.debug('"{0}" does not resolve to any element'.format(part))
        else:
            msgr.debug('"{0}" resolved to: {1}'.format(part, candidates[0]))
            element = candidates.pop(0)
    if not element:
        msgr.message('fatal: cannot define what element to use')
        exit(1)
    # Performing necessary checks
    if not os.path.isfile(os.path.join(scheme_path, scheme, 'elements', element, 'meta.json')):
        msgr.message('fatal: cannot find metadata for element "{0}" in scheme "{1}"'.format(element, scheme))
        exit(1)
    element_meta = bearton.schemes.inspector.getElementMeta(scheme_path, scheme, element)
    msgr.debug('loaded metadata for element from: {0}'.format(os.path.join(scheme_path, scheme, 'elements', element, 'meta.json')))
    if '--base' in ui:
        if 'base' not in element_meta or element_meta['base'] == False:
            msgr.message('fatal: cannot add page as a base element', 0)
            exit(1)
        if element in os.listdir(os.path.join(bearton.util.env.getrepopath(TARGET), 'db', 'base')):
            msgr.message('fatal: base element "{0}" already created: try "bearton page edit -b {0}" command'.format(element), 0)
            exit(1)
    if 'singular' in element_meta:
        if element_meta['singular'] and len(db.query(scheme, element)) > 0:
            msgr.message('failed to create new element of type "{0}": element is singular'.format(element), 0)
            exit(1)
    if 'bare' in element_meta and element_meta['bare']:
        msgr.message('fatal: cannot create db entry for bare element: {0}'.format(element), 0)
        exit(1)

    # Actual call creating new page in database
    creator = (bearton.page.page.newbase if '--base' in ui else bearton.page.page.new)
    hashed = creator(target=bearton.util.env.getrepopath(TARGET), use=(scheme_path, scheme, element), messenger=msgr)
    exit(2)
    if '--edit' in ui: bearton.page.page.edit(path=SITE_PATH, page=hashed, base=('--base' in ui), msgr=msgr)
    else: msgr.message(hashed, 0)
    if '--render' in ui: bearton.page.builder.build(path=SITE_PATH, schemes=SCHEMES_PATH, page=hashed, msgr=msgr)
elif str(ui) == 'edit':
    """This mode is employed for editing existing pages.
    """
    page_id = ''
    if ui.operands(): page_id = ui.operands()[0]
    if '--page-id' in ui: page_id = ui.get('-p')
    if not page_id and '--from-file' not in ui:
        msgr.message('fail: page id is required')
        exit(1)

    ids = ([l.strip() for l in bearton.util.readfile(ui.get('--from-file')).split('\n')] if '-F' in ui else [page_id])
    for i, id in enumerate(ids):
        if id not in db.keys():
            candidates = [k for k in db.keys() if k.startswith(id)]
            if len(candidates) > 1:
                msgr.message('fail: id "{0}" resolves to more than one element'.format(id))
                ids[i] = ''
            elif len(candidates) == 0:
                msgr.message('fail: id "{0}" does not resolve to any element'.format(id))
                ids[i] = ''
            else:
                id = candidates.pop(0)
                ids[i] = id
        if id in db.keys():
            if '--markdown' in ui: bearton.page.page.editmarkdown(SITE_PATH, id, ui.get('-m'), msgr)
            else: bearton.page.page.edit(SITE_PATH, id, ('--base' in ui), msgr)
        else:
            msgr.message('fail: there is no such page as {0}'.format(id))
    if '--render' in ui:
        for i in [i for i in ids if i != '']:
            bearton.page.builder.build(path=SITE_PATH, schemes=SCHEMES_PATH, page=i, msgr=msgr)
elif str(ui) == 'render':
    """This mode is used to render individua pages, groups of pages or whole sites.
    """
    pages = (db.keys() if '--all' in ui else ui.operands())
    if '--type' in ui: pages = [key for key, entry in db.query(scheme=config.get('scheme'), element=ui.get('-t'))]
    existing = db.keys()
    for page in pages:
        if page not in db.keys():
            candidates = [k for k in db.keys() if k.startswith(page)]
            if len(candidates) > 1:
                msgr.message('fail: id "{0}" resolves to more than one element'.format(id))
            elif len(candidates) == 0:
                msgr.message('fail: id "{0}" does not resolve to any element'.format(id))
            else:
                page = candidates.pop(0)
        if page not in existing:
            msgr.message('fail: page "{0}" does not exist'.format(page), 0)
            if page in bearton.schemes.inspector.lselements(scheme=config.get('scheme')):
                msgr.message('note: string "{0}" is a name of an element in currently used scheme:'.format(page), 1)
                msgr.message(' * try \'bearton-db query {0}\' command to obtain IDs of pages created using this type'.format(page), 1)
                msgr.message(' * try \'bearton-page render --type {0}\' command to render all pages of this type'.format(page), 1)
            continue
        else:
            msgr.message('rendering page: {0}'.format(page), 1)
        if '--dry-run' in ui:
            rendered = bearton.page.builder.render(path=SITE_PATH, schemes=SCHEMES_PATH, page=page, msgr=msgr)
            if '--print' in ui: msgr.message(rendered, 0)
        else: bearton.page.builder.build(path=SITE_PATH, schemes=SCHEMES_PATH, page=page, msgr=msgr)
elif str(ui) == 'rm':
    """This mode is used to remove pages from database.
    """
    page_id = ''
    if ui.operands(): page_id = ui.operands()[0]
    if '--page-id' in ui: page_id = ui.get('-p')
    if not page_id:
        msgr.message('fail: page id is required')
        exit(1)
    msgr.message('removing page {0}'.format(page_id), 1)
    warnings.warn('IMPLEMENT ME!')
