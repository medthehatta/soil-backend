import csv
from io import StringIO

import requests
from diskcache import Cache

cache = Cache(__name__)


@cache.memoize()
def map_unit_composition(mukey):
    url = (
        f"https://casoilresource.lawr.ucdavis.edu/soil_web/component_data.php"
    )
    params = {
        "mukey": mukey,
        "action": "component",
        "format": "csv",
    }
    res = requests.get(url, params=params)
    res.raise_for_status()
    csvdata = csv.DictReader(StringIO(res.text.strip()))
    components = [
        {
            "series": c["compname"],
            # FIXME: need to aggregate _l, _r, _h comppcts
            "percent": int(c["comppct_r"]),
            "geomdesc": c["geomdesc"],
            "suborder": c["taxsuborder"],
            "class": c["taxclname"],
        }
        for c in csvdata
        if c["compkind"].lower() == "series"
    ]
    return components
