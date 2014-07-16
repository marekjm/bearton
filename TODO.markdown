## Bearton's TODO list

- improve database querying:
    - support for tags,
    - maybe an alternative SQL-like syntax,
- improve docs,
- create function for getting elements' metadata in a unified manner (this will ensure all required fields are always present and have default value unless overridden by `meta.json` content),

```
bearton-db index        # indexes db
bearton-page purge      # database.paths()
```

- implement generating JSON files,
- wherever `scheme` parameter is used in function calls, it **MUST** be a path to the scheme-directory, e.g. `/usr/share/bearton/schemes/default` because it carries two pieces of information:
  the location and name of the scheme,
