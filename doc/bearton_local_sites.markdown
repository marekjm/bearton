## Bearton Doc: Local Sites

To create Bearton local site (a *repository* of a kind) which contents will be later
sent to the Net, one must use `bearton init` command.

----

### Separation of Bearton and site

Each repository is divided into two parts: *inside* and *outside*.
Inside part of the repository is the hidden `./.breaton` directory containing
database, schemes and configuration.
Outside is everything else.

By default, only outside part is sent to the Net and displayed to site viewers.
However, when full push to the server is done, the database is also sent -
as a compressed tar archive.

**Example site:**

```
index.html
blog.html
blog/
blog/2014/index.html
blog/2014/04/index.html
blog/2014/04/bearton_alpha.html
                                       | outside part
        -------------------------------|-------------
                                       | inside  part
.bearton/
.bearton/schemes/
.bearton/schemes/default/
.bearton/db/
.bearton/db/0123feed4567dead8901deaf2345beef6789
.bearton/db/0123feed4567dead8901deaf2345beef6789/meta.json
.bearton/db/0123feed4567dead8901deaf2345beef6789/context.json
```
