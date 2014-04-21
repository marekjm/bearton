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
        "contexts": [""],
        "base": ["head", "header", "footer"]
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
Each context can be a name (for singular objects) or a query.

Singular contexts are directly merged into main context.  
Query contexts are inserted as a list.

*Query contexts*

If first character of a context is a hashbang - `#` - Bearton will interpret it as a query.

Syntax: `#field:element@scheme&key=value(,key=value)*&tag0,tag1(,tagN)*;`

Elements of the query, except for the first - field name element - are separated by ampersand symbol: `&`.

List of elements:

- `field`: specifies name under which the list resulting from the query will be inserted;
- `element@scheme`: `element` is a name of the element, and `scheme` is the name of the scheme - one may be omitted, omission of both will result in an empty query;
- `key=value(,key=value)`: comma separated list of key/value pairs to form *query dict* (a.k.a. queryd), neither key nor value may contain comma or ampersand characters;
- `tag0,tag1(,tagN)*`: comma separated list of tags to match;

----

**`requires.base`**

This is a list of *base* contexts the element requires to be correctly rendered.
Base contexts are first looked for in the database, if base is not found in the db defaults are
loaded from scheme.  
Such behaviour means that for one-shot schemes, it is reasonable to not to create db entries for
base elements -- because then we remove the need to update database after scheme updates.

----

**`output`**

This is a file path, without preceding slash.
It tells Bearton where to write rendered element.

The path in meta may be formatted using following strings, using `{{foo}}` syntax:

- `year`: expands to year,
- `month`: expands to month of the year,
- `mday`: expands to day of the month,
- `yday`: expands to day of the year,
- `epoch`: expands to number of seconds from epoch,

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
