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

msgr = bearton.util.Messenger()

if str(ui) == 'new':
    if '--scheme' in ui: scheme = ui.get('-s')
    else: scheme = 'default'

    element = (ui.get('-e') if '--element' in ui else '')
    if not element and not ui.arguments:
        print('bearton: fatal: requires element to create new page')
    
    if len(ui.arguments) == 1:
        element = ui.arguments[0]
    elif len(ui.arguments) == 2:
        scheme = ui.arguments[0]
        element = ui.arguments[1]
    elif len(ui.arguments) == 0:
        pass
    else:
        print('bearton: fail: invalid number of operands: maximum is two')

    if '/' in element and len(ui.arguments) == 1:
        parts = element.split('/')
        scheme = parts[0]
        element = parts[1]

    print('scheme:', scheme)
    print('element:', element)

    bearton.page.new(site='./site', scheme=scheme, element=element)
