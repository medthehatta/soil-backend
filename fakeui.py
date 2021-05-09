from tabulate import tabulate
from cytoolz import curry

import appdb


ui_state = {
    "last_num_mapping": None,
}


player_state = {
    "location": None,
    "money": None,
    "inventory": None,
}


@curry
def without_keys(keys, dic):
    return {k: v for (k, v) in dic.items() if k not in keys}


@curry
def without_key(key, dic):
    return {k: v for (k, v) in dic.items() if k != key}


def draw_table(records, sort_by=None, desc=False):
    if sort_by:
        sort_key = lambda x: x[sort_by]
    else:
        sort_key = lambda x: 1
    with_sort = sorted(records, key=sort_key, reverse=desc)
    with_num = [{"i": i, **record} for (i, record) in enumerate(with_sort, 1)]
    id_stripped = [without_key("_id", record) for record in with_num]
    num_mapping = {r["i"]: r for r in with_num}
    ui_state["last_num_mapping"] = num_mapping
    print(tabulate(id_stripped, headers="keys"))


def initialize():
    player_state["inventory"] = appdb.get_items("inventory/0")["items"]
    player_state["money"] = 1000


class TabularUi:

    def __init__(self, records, sort=None, desc=False):
        self.records = records
        self.sort = sort
        self.desc = desc
        self.num_mapping = {}

    def __repr__(self):
        self.draw()
        return super().__repr__()

    def draw(self):
        if self.sort:
            sort_key = lambda x: x[self.sort]
        else:
            sort_key = lambda x: 1
        with_sort = sorted(self.records, key=sort_key, reverse=self.desc)
        with_num = [
            {"i": i, **record} for (i, record) in enumerate(with_sort, 1)
        ]
        id_stripped = [without_key("_id", record) for record in with_num]
        num_mapping = {r["i"]: r for r in with_num}
        self.num_mapping = num_mapping
        print(tabulate(id_stripped, headers="keys"))

    @property
    def rev(self):
        self.desc = not self.desc
        self.draw()

    def __call__(self, i):
        return self.select(i)

    def select(self, i):
        return self.num_mapping.get(i)


class InventoryUi(TabularUi):

    @property
    def n(self):
        self.sort = "name"
        self.draw()

    @property
    def qual(self):
        self.sort = "quality"
        self.draw()

    @property
    def quant(self):
        self.sort = "quantity"
        self.draw()


if __name__ == "__main__":
    initialize()
    inv = InventoryUi(player_state["inventory"])
