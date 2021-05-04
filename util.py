import json
from collections import defaultdict


def slurp_file(path):
    with open(path) as fh:
        return fh.read()


def line_delimit(s):
    return [s.strip() for s in s.splitlines()]


def emit_json(obj, path):
    with open(path, "w") as fh:
        json.dump(obj, fh)


def read_json(path):
    try:
        with open(path) as fh:
            return json.load(fh)
    except NotADirectoryError:
        return None


UNSET = object()

        
def get_at(path, data, default=UNSET):
    if not isinstance(path, (list, tuple)):
        return _get_one(path, data, default)
    else:
        if len(path) == 0:
            raise ValueError("Path must not be empty!")
        else:
            nxt = _get_one(path[0], data, default)
            return _get_at(path[1:], nxt, default)


def _get_one(path, data, default=UNSET):
    try:
        return data[item]
    except LookupError:
        if default is not UNSET:
            return default
        else:
            raise 


def normal_dict(dd):
    if type(dd) is dict:
        return {k: normal_dict(v) for (k, v) in dd.items()}
    elif isinstance(dd, (list, tuple)):
        return type(dd)([normal_dict(x) for x in dd])
    elif isinstance(dd, collections.defaultdict):
        return normal_dict(dict(dd))
    else:
        return dd
