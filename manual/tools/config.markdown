## tool: `bearton-config`

`bearton-config` is used to perform configuration-related tasks, including:

- setting keys in config,
- removing keys from config,
- inspecting configuration,

To see quick help use `bearton-config --help`.
Basic usage:

```
bearton-config <mode> [option...] [operand...]
```

----

### Mode: `set`

Used for setting keys in config.

```
bearton-config set <key> [<value>]
bearton-config set --key <key> [--value <value>]
```

Both commands will set key to value.
Specifying value if optional, in case it is omitted default value (empty string) is used.
Command-set values override oprand-set values.


----

### Mode: `rm`

Used to remove keys from config.

```
bearton-config rm [<key>...]
bearton-config rm [--pop] --key <key>
```

First command will remove any key given as operand from configuration file.
Second command will remove the key but also print its value to screen.

If a key is set with `--key` option it overrides any keys passed as operands.


----

### Mode: `get`

Used to inspect configuration.

```
bearton-config get [--json] <key>
bearton-config get [--json] --key <key>
bearton-config [--verbose] get [--json] --list
```

First and second command will just print value of the key to screen.

Third command will print all keys to the screen.
If `--verbose` option is passed with `--list`, keys will be listed with their respective values.

In each case, `--json` option will cause the result to be JSON encoded.
