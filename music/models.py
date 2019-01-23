# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from django.urls import reverse
from requests import get
from .process_color import *


class Album(models.Model):
    artist = models.CharField(max_length=250)
    album_title = models.CharField(max_length=500)
    genre = models.CharField(max_length=100)
    facebook = models.CharField(max_length=1000)
    color = models.CharField(max_length=10)
    border_color = models.CharField(max_length=15)
    album_logo = models.FileField()

    def __init__(self, *args, **kwargs):
        models.Model.__init__(self, *args, **kwargs)
        if self.album_logo:
            self.define_colors()

    def __str__(self):
        return '{} - {}'.format(self.artist, self.album_title)

    def define_colors(self):
        color_data = get_main_color(self.album_logo.path)
        self.color = color_data[0]
        self.border_color = get_border_color(color_data[1])
        self.save()

    def get_absolute_url(self):
        return reverse('music:detail', kwargs={'pk': self.pk})


class Song(models.Model):
    album = models.ForeignKey(Album, on_delete=models.CASCADE)
    song_title = models.CharField(max_length=250)
    is_favorite = models.BooleanField(default=False)

    def __str__(self):
        return self.song_title
