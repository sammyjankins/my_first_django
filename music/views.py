# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from .models import Album, Song
from django.views.generic.edit import UpdateView
from django.shortcuts import render, get_object_or_404, redirect
from .forms import AlbumForm, SongForm, UserRegForm
from django.contrib import messages
from django.db.models import Q
from django.http import JsonResponse

AUDIO_FILE_TYPES = ['wav', 'mp3', 'ogg']
IMAGE_FILE_TYPES = ['png', 'jpg', 'jpeg']


def index(request):
    if not request.user.is_authenticated:
        return redirect('music:register')
    else:
        albums = Album.objects.filter(user=request.user)
        song_results = Song.objects.all()
        query = request.GET.get("q")
        if query:
            albums = albums.filter(
                Q(album_title__icontains=query) |
                Q(artist__icontains=query)
            ).distinct()
            song_results = song_results.filter(
                Q(song_title__icontains=query)
            ).distinct()
            return render(request, 'music/index.html', {
                'albums': albums,
                'songs': song_results,
            })
        else:
            return render(request, 'music/index.html', {'albums': albums})


def create_album(request):
    if not request.user.is_authenticated:
        return redirect('music:register')
    else:
        form = AlbumForm(request.POST or None, request.FILES or None)
        if form.is_valid():
            album = form.save(commit=False)
            album.user = request.user
            album.album_logo = request.FILES['album_logo']
            file_type = album.album_logo.url.split('.')[-1]
            file_type = file_type.lower()
            if file_type not in IMAGE_FILE_TYPES:
                context = {
                    'album': album,
                    'form': form,
                    'error_message': 'Image file must be PNG, JPG, or JPEG',
                }
                return render(request, 'music/album_form.html', context)
            album.save()
            return render(request, 'music/detail.html', {'album': album})
        context = {
            "form": form,
        }
    return render(request, 'music/album_form.html', context)


def create_song(request, album_id):
    form = SongForm(request.POST or None, request.FILES or None)
    album = get_object_or_404(Album, pk=album_id)
    if form.is_valid():
        albums_songs = album.song_set.all()
        for s in albums_songs:
            if s.song_title == form.cleaned_data.get("song_title"):
                context = {
                    'album': album,
                    'form': form,
                    'error_message': 'You already added that song',
                }
                return render(request, 'music/create_song.html', context)
        song = form.save(commit=False)
        song.album = album
        song.audio_file = request.FILES['audio_file']
        file_type = song.audio_file.url.split('.')[-1]
        file_type = file_type.lower()
        if file_type not in AUDIO_FILE_TYPES:
            context = {
                'album': album,
                'form': form,
                'error_message': 'Audio file must be WAV, MP3, or OGG',
            }
            return render(request, 'music/create_song.html', context)

        song.save()
        return render(request, 'music/detail.html', {'album': album})
    context = {
        'album': album,
        'form': form,
    }
    return render(request, 'music/create_song.html', context)


def detail(request, album_id):
    if not request.user.is_authenticated:
        return redirect('music:register')
    else:
        user = request.user
        album = get_object_or_404(Album, pk=album_id)
    return render(request, 'music/detail.html', {'album': album, 'user': user})


def delete_album(request, album_id):
    album = Album.objects.get(pk=album_id)
    album.delete()
    # albums = Album.objects.filter(user=request.user)
    return redirect('../../')
    # return render(request, 'music/index.html', {'albums': albums})


def favorite_album(request, album_id):
    album = get_object_or_404(Album, pk=album_id)
    try:
        if album.is_favorite:
            album.is_favorite = False
        else:
            album.is_favorite = True
        album.save()
    except (KeyError, Album.DoesNotExist):
        return JsonResponse({'success': False})
    else:
        albums = Album.objects.filter(user=request.user)
        return render(request, 'music/index.html', {'albums': albums})
        # return JsonResponse({'success': True})


def register(request):
    if request.method == 'POST':
        form = UserRegForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, 'Welcome, {}'.format(username))
            return redirect('music:index')
    else:
        form = UserRegForm()
    return render(request, 'music/register.html', {'form': form})


class AlbumUpdate(UpdateView):
    model = Album
    fields = ['artist', 'album_title', 'genre', 'album_logo', 'facebook']
