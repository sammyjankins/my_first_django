# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.views import generic
from .models import Album
from django.views.generic.edit import CreateView, UpdateView, DeleteView


class IndexView(generic.ListView):
    template_name = 'music/music.html'
    context_object_name = 'all_albums'

    def get_queryset(self):
        return Album.objects.all()


class DetailView(generic.DetailView):
    model = Album
    template_name = 'music/detail.html'


class AlbumCreate(CreateView):
    model = Album
    fields = ['artist', 'album_title', 'genre', 'album_logo']
