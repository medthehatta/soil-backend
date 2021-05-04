import json
import random
import os
from collections import defaultdict
from collections import Counter
from contextlib import contextmanager
from importlib import reload
from uuid import uuid1
from types import SimpleNamespace

from cytoolz import memoize

from util import *

import soil_series as ss; reload(ss)
import map_unit as mu; reload(mu)
import parse as pr; reload(pr)
import appdb; reload(appdb)


def uuid():
    return str(uuid1())


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


def random_inventory_1(size):
    random.seed(1)
    result = defaultdict(lambda: defaultdict(list))
    items = (random_soil_item() for _ in range(size))
    for it in items:
        ser = it["series"]
        hor = it["horizon"]
        qly = it["quality"]
        if ser not in result:
            result[ser] = {}
        if hor not in result[ser]:
            result[ser][hor] = []
        result[ser][hor].append(qly)
    return normal_dict(result)


def random_inventory(size):

    item_names = line_delimit(slurp_file("names.txt"))

    def _item():
        name = random.choice(item_names)
        quality = random.randint(10, 1000)
        quantity = random.randint(1, 1000)
        return {"_id": uuid(), "name": name, "quality": quality, "quantity": quantity}

    return sorted([_item() for _ in range(size)], key=lambda x: x["name"])


Item = SimpleNamespace


class RandomMarket:

    def __init__(
        self,
        namefile,
        quantity_range=(1, 10),
        quality_range=(100, 1000),
    ):
        self.item_names = line_delimit(slurp_file("names.txt"))
        self.name_frequencies = Counter(self.item_names)
        total = sum(self.name_frequencies.values())
        self.rarities = {
            k: (1 - v/total)
            for (k, v) in self.name_frequencies.items()
        }
        self.quantity_range = quantity_range
        self.quality_range = quality_range

    def _value(self, item):
        rarity = 1 - self.rarities[item.name]
        quality_factor = item.quality**(3/2)
        rigidity = 4
        fudge = (rigidity + random.random()) / (rigidity + 1)
        return fudge * rarity * quality_factor

    def random_item(self):
        return Item(
            name=random.choice(self.item_names),
            quality=random.randint(*self.quality_range),
        )

    def random_transaction(self):
        give = self.random_item()
        want = self.random_item()
        if give.quality < want.quality:
            (give, want) = (want, give)
        give_quantity = random.randint(*self.quantity_range)
        value_ratio = self._value(give) / self._value(want)
        want_quantity = int(give_quantity * value_ratio)
        return ((give, give_quantity), (want, want_quantity))

    def format_transaction(self, trans):
        ((give, give_quantity), (want, want_quantity)) = trans
        return {
            "_id": uuid(),
            "gives": give.name,
            "quality": give.quality,
            "quantity": give_quantity,
            "wants": want.name,
            "want_quality": want.quality,
            "want_quantity": want_quantity,
        }

    def generate(self, n = 20):
        transactions = [
            self.format_transaction(self.random_transaction())
            for _ in range(n)
        ]
        return transactions
