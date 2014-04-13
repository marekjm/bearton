**Check init**

First, force initializatio of a new Bearton repo in a `./sitebuild` directory, and
copy schemes from `./schemes` directory.  
Then check if the init process was correct by printing JSON-formatted list of keys in
config file.

```
ui/bearton-init.py init -fw ./sitebuild -s ./schemes && ./ui/bearton-config.py get -jlw ./sitebuild
```

----


**Set key with empty value in config**

Apply `-w` (or `--where`) option to set different target directory.

```
ui/bearton-config.py set foo
ui/bearton-config.py set -k foo bar
```

The latter command will set only `foo` key and discard `bar` as options take precendence
over operands.

----


**Set key with non-empty value in config**

Apply `-w` (or `--where`) option to set different target directory.

```
ui/bearton-config.py set foo bar
ui/bearton-config.py set -k foo -v bar
```

----


**Display list of all keys**

Use different target directory with `-w` option.
Apply `-j` (or `--json`) option to get JSON formatted output.

```
1)  ui/bearton-config.py get -lw ./sitebuild
2)  ui/bearton-config.py get -jlw ./sitebuild

1)  ui/bearton-config.py get --list --where ./sitebuild
2)  ui/bearton-config.py get --json --list --where ./sitebuild
```

----


**Display all keys and their values**

Use different target directory with `-w` option.
Apply `-j` (or `--json`) option to get JSON formatted output (this will effectively dump config file).

Adding values to listing is done by passing `-v` (or `--verbose`) option along with `--list`.

```
1)  ui/bearton-config.py get -vlw ./sitebuild
2)  ui/bearton-config.py get -jvlw ./sitebuild

1)  ui/bearton-config.py get --verbose --list --where ./sitebuild
2)  ui/bearton-config.py get --json --verbose --list --where ./sitebuild
```
