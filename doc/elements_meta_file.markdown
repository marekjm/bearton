## Meta data about elements of Bearyon schemes

Bearton sites are built on schemes, which are built from elements.
Element is a template (either partial or full), a context, and a metadata.

Here are described keys which, if found inside element's metadata, carry some meaning
in Bearton.

Ever-up-to-date list of keys can be found in source code of Bearton.

----

### Fully specified meta file

```
{
    "requires": {
        "contexts": ["head", "header", "footer"]
    },
    "output": "index.html",
    "singular": true,
    "base": false
}
```

----

### Keys

**`requires`**

This is a dictionary containing various requirements of this element.
Sub-keys of this dict are described here with preceding `requires.`.

----

**`requires.contexts`**

This is a list of contexts the element requires to be correctly rendered.

----

**`requires.base`**

This is a list of *base* contexts the element requires to be correctly rendered.
Such contexts are first looked for in database.

----

**`output`**

This is a file path, without preceding slash.
It tells Bearton where to write rendered element.

The path in meta may be formatted using following strings, using `{{foo}}` syntax:

- `year`: expands to year,
- `month`: expands to month of the year,
- `month_day`: expands to day of the month,
- `epoch`: expands to number of seconds from epoch,
- `random:N`: expands to `N` random charaters from the set of valid characters for paths, except for directory separator (e.g. `/` on Linux),

Paths may contain:

- lower- and uppercase letters,
- digits,
- hyphen, underscore and dot,

Elements with empty `output` path are considered to be not buildable on their own, and thus
cannot be created as a separate entries in pages database with `bearton page new` command.
They can only be required by other - buildable and unbuildable - elements, or
be added to databse as *base* elements.

----

**`base`**

This specifier means that the file is a base file for the site and
contains data that may be specific for each distribution of the scheme - e.g. menus, slogans, stylesheets etc.

Such elements can be created with `bearton page new` command and are placed in a database directory separate from
ordinary pages.

----

**`singular`**

If set to true, only one such element can be created -- commands to create another such element will fail.
Singular specifier has effects only on buildable elements because only they can create entries in database.
