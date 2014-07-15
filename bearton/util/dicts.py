"""Utility functions to ease operations on dictionaries.
"""

def similarise(base, patch):
    """Copies keys missing in base but present in patch to base dictionary.
    Does not overwrite or update any value already present in base.

    Raises TypeError when the same key has different type in base and update dicts.
    """
    new = {}
    for k, v in base.items(): new[k] = v
    for key in patch:
        if key in base:
            if type(base[key]) != type(patch[key]):
                raise TypeError('different types for key: {0}'.format(key))
            if type(base[key]) == dict:
                new[key] = similarise(base[key], patch[key])
        else:
            new[key] = patch[key]
    return new

def update(base, patch, overwrites=True, allow_ow=[], removals=True):
    """Updates all values present in base with values present in update.
    If `removals` is true, removes all keys that are not present in update.
    Else, leaves them as they were.
    `allow_ow` is a list of keys for which overwrites are allowed.
    """
    new = {}
    for key in base:
        if key in patch:
            if overwrites or key in allow_ow:
                if type(base[key]) == dict and type(patch[key]) == dict: value = update(base[key], patch[key], overwrites, allow_ow, removals)
                else: value = patch[key]
            else: value = base[key]
            new[key] = value
        if key not in patch and not removals:
            new[key] = base[key]
    return new

def merge(base, patch, **kwargs):
    """First similarises and then updates base dict with update dict.
    kwargs are passed to dictupdate() function and are not directly used by dictmerge.
    """
    new = update(base=similarise(base, patch), patch=patch, **kwargs)
    return new
