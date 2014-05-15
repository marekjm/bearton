## tool: `bearton-page`

`bearton-page` is used to perform page-related tasks, including:

- creating new pages,
- editing existing pages,
- rendering pages,

To see quick help use `bearton-page --help`.
Basic usage:

```
bearton-page <mode> [option...] [operand...]
```

----

### Creating new page

Creating new page is done with `bearton-page new` mode.

```
bearton-page new [-s <scheme>] [-e <element>] [--edit] [--render] <element> [<scheme>]
```

There are several ways to create a new page.

**Specifying just the element (simplest way)**

```
bearton-page new foo
```

This will create new page of type `foo` from the scheme set in config.

Feature that is useful when using schemes with long element names, is that if given string does not point
directly to an element Bearton will try to match the name to an element.  
Strings that will match more than one element will result in failure,
just as strings which will not match any element.

For example, following command will create new page of type *article*:

```
bearton-page new art
```

However, if the scheme being used had elements *article* and *articles* - which both would be matched
by the *art* string - this command would result in a failure message.

It is possible to skip the matching by specifying the element explicitly.


**Specifiying both scheme and element**

```
bearton-page new <element> <scheme>
```

This will create new page of type `element` but take the template from scheme `scheme` instead of the one
specified in config.
Usualy it is not needed but can be employed when two schemes are compatible.

**Explicitly specifying element**

```
bearton-page new -e foo bar
```

Without `-e` option Bearton would create new page of type `bar` but options overrides operands so
the final element to use is `foo`.  
Elements specified explicitly will not be matched.

**Explicitly specifying scheme**

```
bearton-page new -s scheme foo
```

Specifying scheme with `-s` option Bearton will override scheme set in config.
This is equivalent to:

```
bearton-page new foo scheme
```

**Explicitly specifying scheme and element**

The explicit options `-s` and `-e` can be used together.
Two following lines are equvalent:

```
bearton-page new foo bar
bearton-page new -e foo -s bar
```

### More options

There are two more options to use when creating pages.

**`--edit`**

This option is used to automatically launch editor and edit the context of the new page just after it is created in the database.

**`--render`**

This option is used to render the page immediatelly after it is created.


Useful command is: `bearton-page new -ER foo`  
It will create new page of type `foo`, launch editor for its context, and render it after the user finishes editing.
This provides for instant publishing of new pages.

----

### Editing existing page

Editing pages can be done with `bearton-page edit` mode.
Multiple ids can be specified with `--from-file` option.

```
bearton-page edit [--page-id <hash>] [--from-file <path>] [--render] [--markdown <what>] <hash>
bearton-page edit [--base] <name>

bearton-page edit <hash>
bearton-page edit --page-id <hash>
bearton-page edit --from-file ./list_of_ids_to_edit.txt
```

It is possible to use first characters of the hash, Bearton will try to resolve them into full ID.

**Editing context of page**

By default, `bearton-page edit` will edit context of the page(s) with supplied id.

**Editing Markdown partials**

This can be achieved with `--markdown` option.

```
bearton-page edit --markdown article <hash>
```

In such case, Bearton will search the `.bearton/db/pages/<hash>/markdown/` directory for:

- `article` file,
- `article.md` file,
- `article.markdown` file,

**Editing base elements**

This is enabled with `--base` option.

**Editor used**

When editing, Bearton will use the editor pointed to by `EDITOR` environment variable and, in case it's not found, default to VIM.

----

### Rendering pages

Rendering of pages is done with `bearton-page render` mode.

```
bearton-page render [--dry-run [--print]] [<hash>...]
bearton-page render [--dry-run [--print]] [--all | --type <name>]

bearton-page render [--dry-run [--print]] $(bearton-db query <query>)
```

This will render page with given ID and write the results to output path specified in meta of the page.
Partial hashes will be resolved to full IDs.

To render all pages: `bearton-page render --all`  
To render all pages *of given type*: `bearton-page render --type <type>`

**Testing and dry-running**

```
bearton-page render --dry-run [--print] <hash>
```

There is a possibility of dry-run the rendering, i.e. perform all of the steps required to render the page except
of the write-to-file part. This is enabled by `--dry-run` option.  
With the `--print` option it is possible to print rendered text to screen (useful for debugging).
