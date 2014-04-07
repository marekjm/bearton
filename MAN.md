## Bearton

Static websites management and generation framework

----

## Synopsis 

```
bearton [mode [submode...] [option...]]
```

### Schemes

```
bearton scheme                          --  get name of currently used schemes
bearton scheme --list                   --  list all available (loadable) schemes
bearton scheme load <scheme>            --  load scheme to start using it (overwrite previously used scheme)
bearton scheme reload                   --  reload currenlty used scheme (e.g. after update)
bearton scheme add <scheme>             --  add new scheme to schemes/ directory
bearton scheme rm <scheme>              --  remove scheme from schemes/ directory
```

### Pages

```
bearton page new <page>                 --  create new <page> and add it to database, <page> is name of the element with defined output,
bearton page rm <page-id>               --  remove <page-id> from database, <page-id> is output path of the page,
bearton page edit <page-id>             --  edit <page-id> in database, <page-id> is output path of the page,
```

### Building

```
bearton build [<page-id>]               --  build website unless <page-id> is specified, then build just this page
                                            website is built incrementally, e.g only databse entries which have timestamp newer then
                                            their output counterparts or entries which have not yet been output are built,
bearton build --rebuild                 --  do not look at timestamps while building website,
```

### Pushing to server

```
bearton push [<server>]                 --  push content to <server>, if <server> is not given - push to all servers,
                                            by default pushing only sends static content that is needed to display the website (HTML, JavaScript, CSS etc.)
bearton push [<server>] --db            --  push databse to <server> or to all severs if <server> is not given,
bearton push [<server>] --everything    --  push database and content,
```

### Cloning and pulling

```
bearton clone <url>                     --  clone website database (if available) from <url>
bearton pull                            --  pull new databse entries from upstream website,
```
