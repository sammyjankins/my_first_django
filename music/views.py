# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render
from .models import Album


def index(request):
    all_albums = Album.objects.all()
    context = {'all_albums': all_albums}
    return render(request, 'music/music.html', context)


def detail(request, album_id):
    context = {'album_id': album_id}
    return render(request, 'music/detail.html', context)
