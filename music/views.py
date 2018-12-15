# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.views import generic
from .models import Album


class IndexView(generic.ListView):
    template_name = 'music/music.html'
    context_object_name = 'all_albums'

    def get_queryset(self):
        return Album.objects.all()


class DetailView(generic.DetailView):
    model = Album
    template_name = 'music/detail.html'
