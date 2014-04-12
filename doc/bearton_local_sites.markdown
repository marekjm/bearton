## Bearton Doc: Local Sites

To create Bearton local site (a *repository* of a kind) which contents will be later
sent to the Net, one must use `bearton init` command.

----

### Layouts

Bearton locals (**local s**ites) may have appear in one of two possible layouts;
`outside` (which is the default) and `inside`.

### *Outside* layout

Outside layout means that Bearton data is outside of the built site.

While rebuilding, everything in `./site` subdirectory is removed and then built.

```
bearton/
    schemes/
    config.json
site/
    index.html
db/
    dead0123beef4567feed8901deaf2345/
        meta.json
        context.json
```

### *Inside* layout

Inside layout means that Bearton data is contained in a hidden directory inside
site directory.

While rebuilding, everything in current working directory - except `.bearton` subdirectory - is
removed and then built.

```
index.html
.bearton/
    schemes/
    db/
        dead0123beef4567feed8901deaf2345/
            meta.json
            context.json
    config.json
```
