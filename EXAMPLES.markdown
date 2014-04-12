**Check init**

First, force initializatio of a new Bearton repo in a `./sitebuild` directory, and
copy schemes from `./schemes` directory.  
Then check if the init process was correct by printing JSON-formatted list of keys in
config file.

```
ui/bearton-init.py init -fw ./sitebuild -s ./schemes && ./ui/bearton-config.py get -jlw ./sitebuild
```
