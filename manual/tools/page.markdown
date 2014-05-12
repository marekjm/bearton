## tool: `bearton-page`

`bearton-page` is used to perform page-related tasks, including:

- creating new pages,
- editing existing pages,
- rendering pages,

To see quick help use `bearton-page --help`.

----

### Creating new page

Creating new page is done with `bearton-page new` mode.
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

There are two more options to use when creating the page.



----

### Editing existing page

----

### Rendering pages
