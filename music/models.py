# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from django.urls import reverse
from .process_color import *

from django.contrib.auth.models import Permission, User


class Album(models.Model):
    user = models.ForeignKey(User, default=1, on_delete=models.SET_NULL, null=True)
    artist = models.CharField(max_length=250)
    album_title = models.CharField(max_length=500)
    genre = models.CharField(max_length=100)
    facebook = models.CharField(max_length=100, blank=True)
    bandcamp = models.CharField(max_length=100, blank=True)
    lastfm = models.CharField(max_length=100, blank=True)
    color = models.CharField(max_length=10)
    border_color = models.CharField(max_length=15)
    album_logo = models.FileField()
    is_favorite = models.BooleanField(default=False)

    def __init__(self, *args, **kwargs):
        models.Model.__init__(self, *args, **kwargs)
        if self.album_logo:
            self.define_colors()

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


class Song(models.Model):
    album = models.ForeignKey(Album, on_delete=models.CASCADE, null=True)
    audio_file = models.FileField(default='')
    song_title = models.CharField(max_length=250)
    is_favorite = models.BooleanField(default=False)

    def __str__(self):
        return self.song_title
