import random
from typing import Optional, List
import json
from functools import partial

from cytoolz import unique

from fastapi import FastAPI, Body, Query, Request
from pydantic import BaseModel

from b64query import Base64QueryManager

from util import slurp_file, line_delimit, read_json
import appdb
import soil_series as ss
import map_unit as mu

app = FastAPI()
bq = Base64QueryManager(app)


@app.get("/")
def _():
    return {"Hello": "world"}


@app.get("/market")
def _(
    sort_column: Optional[str] = None,
    desc: bool = False,
):
    collection = f"market"
    data = appdb.get_items(collection, sort_column=sort_column, reverse=desc)
    return {
        "data": data["items"],
        "_fields": data["fields"],
        "_links": {},
    }


@app.get("/legacy-inventory/{uid}")
def _(uid: int):
    inv = read_json("inv.json")
    names = (i["name"] for i in inv)
    query = list(unique(n.rsplit("|", 1)[0] for n in names))
    return {
        "inventory": inv,
        "_links": {
            "series_query": bq.series_query(query),
        },
    }


@app.get("/inventory/{uid}")
def _(
    uid: int,
    sort_column: Optional[str] = None,
    desc: bool = False,
):
    collection = f"inventory/{uid}"
    data = appdb.get_items(collection, sort_column=sort_column, reverse=desc)
    return {
        "data": data["items"],
        "_fields": data["fields"],
        "_links": {},
    }


@app.get("/inventory/{uid}/{iid}")
def _(uid: int, iid: str):
    collection = f"/inventory/{uid}"
    data = appdb.get_item_by_id(collection, iid)
    if data:
        return {
            "data": data["item"],
            "_fields": data["fields"],
            "_links": {},
        }
    else:
        return {"error": f"Could not find item {iid} in inventory {uid}"}


@app.post("/soil-series/query")
def _(names: List[str], aslist: Optional[bool] = False):
    if aslist:
        return ss.multiple_soil_series(names)
    else:
        return ss.soil_series_dict(names)


@app.get("/soil-series/b64/{query}")
@bq.register
def series_query(query: str):
    return ss.soil_series_dict(query)
