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
    album_logo = models.CharField(max_length=1000)
    file_type = models.CharField(max_length=10)
    facebook = models.CharField(max_length=1000)
    color = models.CharField(max_length=10)
    border_color = models.CharField(max_length=15)

    def __init__(self, *args, **kwargs):
        models.Model.__init__(self, *args, **kwargs)
        if self.album_logo[:4] == 'http':
            self.store_logo()

    def store_logo(self):
        resource = get(self.album_logo)
        file = '/home/sammyjankins/PycharmProjects/my_first_django/music/static/music/images/img{}.jpg'. \
            format(self.pk)
        out = open(file, 'wb')
        out.write(resource.content)
        out.close()
        self.album_logo = "../../static/music/images/img{}.jpg".format(self.pk)
        color_data = get_main_color(file)
        self.color = color_data[0]
        self.border_color = get_border_color(color_data[1])
        self.save()

    def get_absolute_url(self):
        return reverse('music:detail', kwargs={'pk': self.pk})

    def __str__(self):
        return '{} - {}'.format(self.artist, self.album_title)


class Song(models.Model):
    album = models.ForeignKey(Album, on_delete=models.CASCADE)
    song_title = models.CharField(max_length=250)
    is_favorite = models.BooleanField(default=False)

    def __str__(self):
        return self.song_title
