import json
from functools import partial
import os
from itertools import zip_longest

from util import slurp_file, line_delimit, read_json, emit_json

DATA_PREFIX = "db"


def _collection(collection):
    return os.path.join(DATA_PREFIX, collection.lstrip("/"))


def castable_to(type_, x):
    try:
        type_(x)
        return True
    except (ValueError, TypeError):
        return False


def _matches(key, entry):
    for (k, e) in zip_longest(key, entry):
        if k == e:
            continue
        elif k == "#" and castable_to(int, e):
            continue
        else:
            return False
    # All fields in the zip matched
    return True


def schema_for(collection):
    entry = collection.lstrip("/").split("/")
    path = _collection("schemas")
    schemas = read_json(path)
    schema_keys = [tuple(x.split("/")) for x in schemas.keys()]

    schema_key = next(
        (key for key in schema_keys if _matches(key, entry)),
        None,
    )

    if schema_key:
        return schemas["/".join(schema_key)]
    else:
        return {}


def get_items(collection, sort_column=None, reverse=False):
    path = _collection(collection)
    items = read_json(path)
    schema = schema_for(collection)
    fields = schema.get("fields", [])

    if sort_column:
        s_items = sorted(items, key=lambda x: x[sort_column], reverse=reverse)
    else:
        s_items = items

    return {"items": s_items, "fields": fields}


def get_item_by_id(collection, id_):
    items = get_items(collection)
    found = next(
        (it for it in items["items"] if it["_id"] == id_),
        None,
    )
    if found:
        return {"item": found, "fields": items["fields"]}
    else:
        return None


def set_items(collection, items):
    path = _collection(collection)
    try:
        os.makedirs(path, exist_ok=True)
    except FileExistsError:
        pass
    emit_json(items, path)


def append_item(collection, item):
    path = _collection(collection)
    items = read_json(path)
    items.append(item)
    emit_json(item_data, path)


def remove_item(collection, item):
    path = _collection(collection)
    items = read_json(path)
    try:
        items.remove(item)
    except ValueError:
        return {"success": False}
    else:
        emit_json(item_data, path)
        return {"success": True}


def remove_item_by_id(collection, id_):
    path = _collection(collection)
    items = read_json(path)
    matching_item = next(
        (it for it in item_data if id["_id"] == id_),
        None,
    )
    if matching_item:
        items.remove(item)
        emit_json(items, path)
        return {"success": True}
    else:
        return {"success": False}
