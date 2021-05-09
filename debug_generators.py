import random
from collections import Counter
import uuid as uuidlib
from types import SimpleNamespace

from util import *


def random_inventory(size):

    item_names = line_delimit(slurp_file("names.txt"))

    def _item():
        name = random.choice(item_names)
        quality = random.randint(10, 1000)
        quantity = random.randint(1, 1000)
        return {"_id": uuid(), "name": name, "quality": quality, "quantity": quantity}

    return sorted([_item() for _ in range(size)], key=lambda x: x["name"])


Item = SimpleNamespace


class RandomMarketGenerator:

    def __init__(
        self,
        namefile,
        quantity_range=(1, 10),
        quality_range=(100, 1000),
    ):
        self.item_names = line_delimit(slurp_file(namefile))
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
        price = int(self._value(give))
        return (give, price)

    def format_transaction(self, trans):
        (give, price) = trans
        return {
            "_id": uuid(),
            "gives": give.name,
            "quality": give.quality,
            "price": price,
        }

    def generate(self, n = 20):
        transactions = [
            self.format_transaction(self.random_transaction())
            for _ in range(n)
        ]
        return transactions


