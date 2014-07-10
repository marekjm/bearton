## tool: `bearton-db`

### Specifying custom format

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


### Defining raw queries

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
