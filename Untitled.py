#!/usr/bin/env python
# coding: utf-8

# In[32]:


import os
from collections import Counter


# In[1]:


from PIL import Image, ImageChops

def trim(im):
    bg = Image.new(im.mode, im.size, im.getpixel((0,0)))
    diff = ImageChops.difference(im, bg)
    diff = ImageChops.add(diff, diff, 2.0, -100)
    #Bounding box given as a 4-tuple defining the left, upper, right, and lower pixel coordinates.
    #If the image is completely empty, this method returns None.
    bbox = diff.getbbox()
    if bbox:
        return im.crop(bbox)

def trim_file(path):
    return trim(Image.open(path))


# In[55]:


from PIL import Image, ImageChops

def trim(im_):
    im = im_.convert("RGBA")
    (w, h) = im.size

    # Create xim, which is the image but in RGBA and with a transparent background
    bgcolor_candidates = [
        im.getpixel(x) for x in [(0, 0), (0, h - 1), (w - 1, 0), (w - 1, h - 1)]
    ]
    (bgcolor, _) = Counter(bgcolor_candidates).most_common(1)[0]
    transparent_bg = (
        (0, 0, 0, 0) if pixel == bgcolor else pixel
        for pixel in im.getdata()
    )
    xim = Image.new("RGBA", im.size, (0, 0, 0, 0))
    xim.putdata(list(transparent_bg))

    # Compute bbox and crop
    bbox = xim.getbbox()
    if bbox:
        return xim.crop(bbox)
    else:
        return xim

def trim_file(path):
    return trim(Image.open(path))


# In[23]:


spritedir = "C:/Users/Med/Desktop/godot/proto/soil1/Images/ezgif-6-6160e028735c-png-99x93-sprite-png/"

def _sprite(name):
    return os.path.join(spritedir, name)

listing = os.listdir(spritedir)
pngs = [x for x in listing if x.endswith(".png") and x.startswith("tile")]


# In[56]:


orders = "alfs ands ids ents els ists epts olls ox ods ults erts".split()
subs = (
    "wass aqu orth ud ust xer torr cry gel hum vitr fluv psamm "
    "turb rend alb per fibr hem sapr fol "
    "sal dur gyps arg calc camb misc1 misc2 misc3"
).split()
taxa = [f"{s}{o}" for o in orders for s in subs]


# In[57]:


tilemap = {f"tile{i:03}.png": f"{tax}.png" for (i, tax) in enumerate(taxa)}


# In[54]:


for (src, dest) in tilemap.items():
    trim_file(_sprite(src)).save(_sprite(dest))


# In[ ]:




