#!/usr/bin/env python
from operator import mul
from functools import reduce
from PIL import Image


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
            if c[0] > max_occurence and ((130 < hsl[1] < 200) and hsl[2] > -1):
                (max_occurence, most_present) = c
        if most_present == 0:
            most_present = (59, 89, 152)
        main_color = most_present
    except TypeError:
        return '#3b5998'
    return ['#' + rgb_to_hex(*main_color), rgb_to_hls(*main_color)[0]]


def get_border_color(hue):
    if hue < 0.111:
        return 'danger'
    elif 0.111 <= hue < 0.194:
        return 'warning'
    elif 0.194 <= hue < 0.388:
        return 'success'
    elif 0.388 <= hue < 0.527:
        return 'info'
    elif 0.527 <= hue < 0.722:
        return 'primary'
    else:
        return 'dark'


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
