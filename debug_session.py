import json
import random
import os
from collections import defaultdict
from collections import Counter
from contextlib import contextmanager
from importlib import reload
from types import SimpleNamespace
from pprint import pprint

from cytoolz import memoize

from util import *

import soil_series as ss; reload(ss)
import map_unit as mu; reload(mu)
import parse as pr; reload(pr)
import appdb; reload(appdb)
import fakeui; reload(fakeui)


@memoize
def some_map_units():
    with open("mus.json") as fh:
        return json.load(fh)


def random_soil_item():
    mu = random.choice(some_map_units())
    component = random.choice(mu)
    series = component["series"]
    profile = ss.soil_series(series)["profile"]
    if profile:
        (horizon, _, _) = random.choice(profile)
    else:
        horizon = "N/A"
    quality = random.randint(10, 1000)
    return {"series": series, "horizon": horizon, "quality": quality}
