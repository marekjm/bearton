"""Utility functions to ease operations on dictionaries.
"""

def similarise(base, update):
    """Copies keys missing in base but present in update to base dictionary.
    Does not overwrite or update any value already present in base.

    Raises TypeError when the same key has different type in base and update dicts.
    """
    new = {}
    for k, v in base.items(): new[k] = v
    for key in update:
        if key in base:
            if type(base[key]) != type(update[key]):
                raise TypeError('different types for key: {0}'.format(key))
            if type(base[key]) == dict:
                new[key] = dictsimilarise(base[key], update[key])
        else:
            new[key] = update[key]
    return new

def update(base, update, overwrites=True, allow_ow=[], removals=True):
    """Updates all values present in base with values present in update.
    If `removals` is true, removes all keys that are not present in update.
    Else, leaves them as they were.
    `allow_ow` is a list of keys for which overwrites are allowed.
    """
    new = {}
    for key in base:
        if key in update:
            if overwrites or key in allow_ow:
                if type(base[key]) == dict and type(update[key]) == dict: value = dictupdate(base[key], update[key], overwrites, allow_ow, removals)
                else: value = update[key]
            else: value = base[key]
            new[key] = value
        if key not in update and not removals:
            new[key] = base[key]
    return new

def merge(base, update, **kwargs):
    """First similarises and then updates base dict with update dict.
    kwargs are passed to dictupdate() function and are not directly used by dictmerge.
    """
    new = dictupdate(base=dictsimilarise(base, update), update=update, **kwargs)
    return new
