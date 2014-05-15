## tool: `bearton-init`

`bearton-init` is used to perform initializatio-related tasks, including:

- initialization,
- reinitialization,
- deinitialization (a.k.a. removal),

To see quick help use `bearton-init --help`.

----

### Initializing a repository

Initializization is performed with `bearton-init init` mode.
It should be accompanied by `--schemes` option to point it to a directory from which schemes should be copied.
Alternatively, it can be supplied with `--no-schemes` option, in whcih case Bearton will not try to copy any schemes.

```
bearton-init init [--schemes <path> | --no-schemes] [--target <path>]
```

`--target` option should be used only for testing purposes:

----

### Updating a repository

Sometimes, a newer version of Bearton introduces changes to the repository structure.
These are additive in their nature so repositories should never *lose* any information,
only *gain* it.  
If an update would cause *loss of information* there will be appropriate guides posted on how
to manually update the repo to preserve the information.

The command to run the update is as follows: `bearton-init init --update`

----

### Reinitializing a repository

Reinitialization process is akin to updating, but will always *lose all information* that has been created as
it wipes the repository clean before creating a new one.

The command is: `bearton-init init --clean`

----

### Removing a repository

There are two ways of removing the repository.

**With `rm` mode**

The command is pretty self-explanatory: `bearton-init rm`  
It will also report on (un)successful removal outcome.

**With `init` mode**

This method is not as straightforward as the former, but has equal functionality: `bearton-init --clean --no-write`  
It will not, however, display any information about whether the removal was successful or not.

This method works by exploting the fact that the `--clean` option tells Bearton to remove the repository (as with reinitialization
process) and later Bearton sees that the `--no-write` option is specified so it does not write anything, and this results in the
repository being removed.

**Checking if removal was successful**

To check if the removal was successful, run `bearton-db query`.
If it complains about not being in a repository then the removal was successful.

Note that in a *very strange* scenarios this may be tricky if one Bearton repo was nested in another.
If it is so, Bearton will treat the parent repository as the target one.
This should be easily spotted, though, because strange/unexpected output will be displayed (`--with-output` option
can be used to display output paths for db entries to make spotting errors even easier).  
The author does not see a resonable use-case for such configuration but it may be encountered in the wild.

----

### Updating schemes

This is done with `bearton-init sync` mode.
With `--schemes` option supplied Bearton will be pointed to a directory containing schemes and
will overwrite schemes in its existing path with the ones from provided path.

By default, overwrite process will only affect already present schemes but `--all` option
will cause all new schemes to be copied.
