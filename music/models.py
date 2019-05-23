# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from django.urls import reverse
from .process_color import *

from django.contrib.auth.models import Permission, User

WEBSITE_NAMES = [
    'bandcamp',
    'soundcloud',
    'spotify',
    'itunes',
    'facebook',
    'vk',
]


class Album(models.Model):
    user = models.ForeignKey(User, default=1, on_delete=models.SET_NULL, null=True)
    artist = models.CharField(max_length=250)
    album_title = models.CharField(max_length=500)
    genre = models.CharField(max_length=100)
    website_1 = models.CharField(max_length=100, blank=True)
    website_2 = models.CharField(max_length=100, blank=True)
    website_3 = models.CharField(max_length=100, blank=True)
    website_4 = models.CharField(max_length=100, blank=True)
    website_5 = models.CharField(max_length=100, blank=True)
    color = models.CharField(max_length=10)
    border_color = models.CharField(max_length=15)
    album_logo = models.FileField()
    is_favorite = models.BooleanField(default=False)

    def __init__(self, *args, **kwargs):
        models.Model.__init__(self, *args, **kwargs)
        self.webInstances = []
        self.webSites = set()
        if self.album_logo:
            self.define_colors()
        if len(self.webInstances) == 0:
            self.set_websites()

    def __str__(self):
        return '{} - {}'.format(self.artist, self.album_title)

    def define_colors(self):
        color_data = get_main_color(self.album_logo.path)
        if color_data == 'white':
            self.color = '#ffffff'
            self.border_color = 'white'
        else:
            self.color = color_data[0]
            self.border_color = get_border_color(color_data[1])
        self.save()

    def get_absolute_url(self):
        return reverse('music:detail', kwargs={'pk': self.pk})

    def set_websites(self):
        inputs = [self.website_1, self.website_2, self.website_3, self.website_4, self.website_5]
        for inp in inputs:
            if inp:
                lnk = inp[inp.find('.') + 1:inp.find('.com')]
                if lnk == '':
                    lnk = inp[inp.find('://') + 3:inp.find('.com')]
                weblink = WebLink(url=inp, website=lnk)
                if lnk in WEBSITE_NAMES:
                    if weblink.website not in self.webSites:
                        self.webInstances.insert(0, weblink)
                        self.webSites.add(weblink.website)
                else:
                    weblink.website = 'link'
                    if weblink.website not in self.webSites:
                        self.webInstances.append(weblink)
                        self.webSites.add(weblink.website)
        self.save()


class Song(models.Model):
    album = models.ForeignKey(Album, on_delete=models.CASCADE, null=True)
    audio_file = models.FileField(default='')
    song_title = models.CharField(max_length=250)
    is_favorite = models.BooleanField(default=False)

    def __str__(self):
        return self.song_title


class WebLink(models.Model):
    url = models.CharField(max_length=100)
    website = models.CharField(max_length=100)

    def __init__(self, url, website, *args, **kwargs):
        models.Model.__init__(self, *args, **kwargs)
        self.url = url
        self.website = website
