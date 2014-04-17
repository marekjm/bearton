import json
import os
from sys import argv

import clap

import bearton


# Building UI
args = clap.formater.Formater(argv[1:])
args.format()

builder = clap.builder.Builder('{0}.json'.format(os.path.splitext(__file__)[0]), argv=list(args))
builder.build()

ui = builder.get()
ui.check()
ui.parse()



# Setting constants for later use
SITE_PATH = (ui.get('-t') if '--target' in ui else '.')
SITE_DB_PATH = os.path.join(SITE_PATH, '.bearton', 'db')
SCHEMES_PATH = (ui.get('-S') if '--schemes-path' in ui else os.path.join(SITE_PATH, '.bearton', 'schemes'))


# Creating widely used objects
msgr = bearton.util.Messenger(verbosity=0, debugging=('--debug' in ui), quiet=('--quiet' in ui))
db = bearton.db.Database(path=SITE_PATH).load()
config = bearton.config.Configuration(path=SITE_PATH).load(guard=True)


# -----------------------------
#   UI logic code goes HERE!  |
# -----------------------------


# Storing widely used objects state
config.store().unload()
db.store().unload()
