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
            if c[0] > max_occurence and ((100 < hsl[1] < 200) and (-0.2 > hsl[2] > -1)):
                (max_occurence, most_present) = c
        if most_present == 0:
            return 'white'
        main_color = most_present
    except TypeError:
        return 'white'
    return ['#' + rgb_to_hex(*main_color), rgb_to_hls(*main_color)[0]]


COLORS = {
    'blue': (0.5862745098039216, 0.6333333333333333),  # 007bff
    'indigo': (0.6333333333333333, 0.7137254901960784),  # 6610f2
    'purple': (0.7137254901960784, 0.8052287581699346),  # 6f42c1
    'pink': (0.8052287581699346, 0.919607843137255),  # e83e8c
    'red': (0.919607843137255, 1),  # dc3545
    'red1': (0, 0.024836601307189548),  # dc3545
    'orange': (0.024836601307189548, 0.11372549019607843),  # fd7e14
    'yellow': (0.11372549019607843, 0.2333333333333333),  # ffc107
    'green': (0.2333333333333333, 0.39999999999999997),  # 28a745
    'teal': (0.39999999999999997, 0.50),  # 20c997
    'cyan': (0.50, 0.5862745098039216)  # 17a2b8
}


def get_border_color(hue):
    for key, value in COLORS.items():
        if value[0] <= hue < value[1]:
            return key


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
