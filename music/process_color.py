#!/usr/bin/env python
from operator import mul
from functools import reduce
from PIL import Image
from colorsys import rgb_to_hls


def prod(iterable):
    return reduce(mul, iterable, 1)


def rgb_to_hex(r, g, b):
    return ''.join(['{:02X}'.format(x) for x in [max(0, min(y, 255)) for y in (r, g, b)]])


def get_main_color(img_path):
    image = Image.open(img_path)
    colors = image.getcolors(prod(image.size))
    max_occurence, most_present = 0, 0
    try:
        for c in colors:
            hsl = rgb_to_hls(*c[1])
            if c[0] > max_occurence and (hsl[1] > 60 and hsl[2] > -1):
                (max_occurence, most_present) = c
        if most_present == 0:
            most_present = (59, 89, 152)
        main_color = most_present
    except TypeError:
        return '#3b5998'
    return '#' + rgb_to_hex(*main_color)


def rgb_to_hls(r, g, b):
    maxc = max(r, g, b)
    minc = min(r, g, b)
    # XXX Can optimize (maxc+minc) and (maxc-minc)
    l = (minc + maxc) / 2.0
    if minc == maxc:
        return 0.0, l, 0.0
    if l <= 0.5:
        s = (maxc - minc) / (maxc + minc)
    else:
        try:
            s = (maxc - minc) / (2.0 - maxc - minc)
        except ZeroDivisionError:
            s = 0
    rc = (maxc - r) / (maxc - minc)
    gc = (maxc - g) / (maxc - minc)
    bc = (maxc - b) / (maxc - minc)
    if r == maxc:
        h = bc - gc
    elif g == maxc:
        h = 2.0 + rc - bc
    else:
        h = 4.0 + gc - rc
    h = (h / 6.0) % 1.0
    return h, l, s
