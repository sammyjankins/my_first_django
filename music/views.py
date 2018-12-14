# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.http import HttpResponse
from .models import Album

def index(request):
    all_albums = Album.objects.all()
    html = ''
    for album in all_albums:
        url = '/music/{}/'.format(album.id)
        html += '<a href="{}">{}</a><br>'.format(url, album.album_title)
    return HttpResponse(html)


def detail(request, album_id):
    return HttpResponse('<h2>Details for album {}: </h2>'.format(album_id))
