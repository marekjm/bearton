## tool: `bearton-db`

`bearton-db` is used to perform db-related tasks, including:

- querying the database of created pages,
- updating the database,
- wiping the database out,

To see quick help use `bearton-db --help`.
Basic usage:

```
bearton-db <mode> [option...] [operand...]
```

----

### Mode: `query`

Used for querying the database.

```
bearton-db query [--with-output]
bearton-db query [--with-output] <element>
bearton-db query [--with-output] <scheme> <element>

bearton-db query [-s <scheme>] [-e <element>] 

bearton-db --verbose query --format "<format>" <element>
bearton-db query --raw "<query>"
```

First command will list all IDs present in database.  
Second command will list only pages with type `<element>`.  
Third will list only pages from scheme `<scheme>` and with type `<element>`.  
If `--with-output` option is present, output path of each page will be displayed alongside its ID.

Options `-s/--scheme` and `-e/--element` allow for explicit specifing of scheme and element.
They also override scheme and element given as operands.


#### Specifying custom format

By default, Bearton will use precomposed signatures, expand them with data it got from the query and
print the resulting string.
This is done for all entries matching the query.

Specifying custom format of print is only available when `--verbose` option is passed and
is set with `--format` option.

Default signature with `--verbose` option is: 
This results in something like this: `de24ad81be63ef26: element@scheme`  
The `--with-output` option appends following string to the signature: 

**How to format output string:**

Substitution strings come in this form: `{:key@from}`.

- `key` can be anything (as long as it matches the regex used to detect subst-strings, check source code for exact pattern used),
- `from` can be empty string, `meta` or `context`,

To get the actual ID of the page use the special form `{:key@}`.
This is separately recognized because `key` is not present in either meta or context.

**Example signatures:**

- with `--verbose` option: `{:key@}: {:name@meta}@{:scheme@meta}`,
- with `--with-output` option: `{:output@meta}` (this is appended to signature),
- default signature: `{:key@}`,


#### Defining raw queries

It is possible to employ the query-engine of Bearton databases directly by passing the raw queries with `--raw` option.

**Structure of raw queries**

Syntax: `#element@scheme&key=value&tag`

Explanations:

- query starts with a hashbang: `#`,
- `element` specifies type of page to be matched,
- `scheme` specifies scheme to be matched,
- query may contain multiple, comma-separated `key=value` pairs specifying key/value pairs in meta to be matched,
- query may contain multiple, comma-separated `tag`s (tags are currently not implemented),

The function that analyses and translates these queries is *very* dumb so the syntax must be followed closely.
No escapes are supported. Ampersands can not be used for purposes other than dividing parts of the query.


----

### Mode: `update`

Used to update the database.

```
bearton-db update [--context-edits-log <path>]
bearton-db update --erase [--yes]
```

**Updating**

Updating database will update contexts of the entries already present.
This should not be needed for base elements - e.g. menus, footers, headers - as they should be standardized.
To decrease the possibility of page elements needing a context update fast-changing elements of pages shall
be stored as Markdown partials.

Only highly template-able parts of pages *should* be implemented to rely heavily on Mustache.
This includes standardized descritions of books, products, software etc., tables, lists and like elements.

Articles shall be always implemented as Markdown partials.

In case a context update requiring manual changes was done, the ID of page will be put into log file.

**Erasing**

Database can be erased with `--erase` option.
Bearton will then ask user if they really want to do it, `--yes` option may be passed with `--erase`
to skip the confirmation step.
