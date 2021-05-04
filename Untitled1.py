#!/usr/bin/env python
# coding: utf-8

# In[2]:


from importlib import reload
import re
import random


# In[44]:


import soil_series as ss; reload(ss)
import map_unit as mu; reload(mu)
import parse as pr; reload(pr)


# In[45]:


ss.soil_series("Flomaton")


# In[50]:


some_map_units = [mu.map_unit_composition(i) for i in range(1914759, 1914850)]


# In[47]:


some_map_units[3]


# In[49]:


ss.soil_series("Codorus")


# In[145]:


import json
with open("mus.json", "w") as fh:
    json.dump(some_map_units, fh)


# In[51]:


import json
import random
import os
from functools import cache
from collections import defaultdict
from contextlib import contextmanager

random.seed(1)


@cache
def some_map_units():
    with open("mus.json") as fh:
        return json.load(fh)


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


def normal_dict(dd):
    if type(dd) is dict:
        return {k: normal_dict(v) for (k, v) in dd.items()}
    elif isinstance(dd, (list, tuple)):
        return type(dd)([normal_dict(x) for x in dd])
    elif isinstance(dd, collections.defaultdict):
        return normal_dict(dict(dd))
    else:
        return dd

def random_inventory(size):
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


# In[58]:


inv = random_inventory(400)


# In[59]:


with open("inv.json", "w") as fh:
    json.dump(inv, fh)
inv


# In[15]:


ss.soil_series("Cowee")


# In[10]:


ss.soil_series("Craigsville")


# In[60]:


mu.map_unit_composition(1914762)


# In[61]:


ss.soil_series("Kinkora")


# In[4]:


foo = ss.soil_series("Kinkora")["class"]


# In[6]:


foo.strip().rsplit(" ", 1)


# In[11]:


ss.suborder_from_full_taxon(foo)


# In[40]:


ss.soil_series("Kinkora")


# In[64]:


ss.soil_series("Exchequer")  # TODO: Trying to parse regolith depth


# In[63]:


import soil_series as ss; reload(ss)
import map_unit as mu; reload(mu)
import parse as pr; reload(pr)


# In[27]:


import os


# In[35]:


open("x", "a").close()
with open("x") as fh:
    json.load(fh)


# In[41]:


lst = []
lst[1:]


# In[70]:


from base64 import b64decode, b64encode


# In[73]:


b64encode(json.dumps(["San Joaquin", "Dulles"]).encode("utf-8")).decode("utf-8")


# In[ ]:




