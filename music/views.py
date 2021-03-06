# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from .models import Album, Song, User, add_demo_albums
from django.shortcuts import render, get_object_or_404, redirect
from .forms import AlbumForm, SongForm, UserRegForm
from django.contrib import messages
from django.db.models import Q
from django.http import JsonResponse
from os import remove
import eyed3

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
                Q(song_title__icontains=query) &
                Q(album__user=request.user)
            ).distinct()
            return render(request, 'music/index.html', {
                'albums': albums,
                'songs': song_results,
                'q': query,
            })
        else:
            return render(request, 'music/index.html', {'albums': albums, 'favs': 'all'})


def fav_albums(request):
    if not request.user.is_authenticated:
        return redirect('music:register')
    else:
        albums = Album.objects.filter(user=request.user, is_favorite=True)
        return render(request, 'music/index.html', {'albums': albums, 'favs': 'favs'})


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
    if not request.user.is_authenticated:
        return redirect('music:register')
    else:
        form = SongForm(request.POST or None, request.FILES or None)
        album = get_object_or_404(Album, pk=album_id)
        if form.is_valid():
            for obj in request.FILES.getlist('audio_files'):
                albums_songs = album.song_set.all()
                song = Song()
                song.album = album
                song.audio_file = obj
                # grabbing song title from ID3 tags
                song.song_title = eyed3.load(obj.temporary_file_path()).tag.title
                for s in albums_songs:
                    if s.song_title == song.song_title:
                        context = {
                            'album': album,
                            'form': form,
                            'error_message': 'You already added that song - {}'.format(song.song_title),
                        }
                        return render(request, 'music/create_song.html', context)
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
    if not request.user.is_authenticated:
        return redirect('music:index')
    else:
        album = Album.objects.get(pk=album_id)
        albums_songs = album.song_set.all()
        for song in albums_songs:
            remove(song.audio_file.path)
        remove(album.album_logo.path)
        album.delete()
        return redirect('music:index')


def delete_song(request, album_id, song_id, current_template):
    if not request.user.is_authenticated:
        return redirect('music:register')
    else:
        album = get_object_or_404(Album, pk=album_id)
        song = Song.objects.get(pk=song_id)
        remove(song.audio_file.path)
        song.delete()
        if current_template == 'songs':
            song_ids = []
            for album in Album.objects.filter(user=request.user):
                for song in album.song_set.all():
                    song_ids.append(song.pk)
            users_songs = Song.objects.filter(pk__in=song_ids)
            return render(request, 'music/songs.html', {'song_list': users_songs})
        else:
            return render(request, 'music/detail.html', {'album': album})


def favorite(request, song_id, current_template):
    if not request.user.is_authenticated:
        return redirect('music:register')
    else:
        song = get_object_or_404(Song, pk=song_id)
        album = song.album
        try:
            if song.is_favorite:
                song.is_favorite = False
            else:
                song.is_favorite = True
            song.save()
        except (KeyError, Song.DoesNotExist):
            return JsonResponse({'success': False})
        else:
            if current_template == 'songs':
                song_ids = []
                for album in Album.objects.filter(user=request.user):
                    for song in album.song_set.all():
                        song_ids.append(song.pk)
                users_songs = Song.objects.filter(pk__in=song_ids)
                return render(request, 'music/songs.html', {'song_list': users_songs})
            else:
                return render(request, 'music/detail.html', {'album': album})


def favorite_album(request, album_id, current_template):
    if not request.user.is_authenticated:
        return redirect('music:register')
    else:
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
            if current_template == 'index':
                albums = Album.objects.filter(user=request.user)
                return render(request, 'music/index.html', {'albums': albums})
            else:
                return render(request, 'music/detail.html', {'album': album})


def register(request):
    if request.method == 'POST':
        form = UserRegForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, 'Welcome, {}'.format(username))
            add_demo_albums(User.objects.get(username=username))
            return redirect('music:login')
    else:
        form = UserRegForm()
    return render(request, 'music/register.html', {'form': form})


def songs(request, filter_by):
    if not request.user.is_authenticated:
        return redirect('music:register')
    else:
        try:
            song_ids = []
            for album in Album.objects.filter(user=request.user):
                for song in album.song_set.all():
                    song_ids.append(song.pk)
            users_songs = Song.objects.filter(pk__in=song_ids)
            if filter_by == 'favorites':
                users_songs = users_songs.filter(is_favorite=True)
        except Album.DoesNotExist:
            users_songs = []
        return render(request, 'music/songs.html', {
            'song_list': users_songs,
            'filter_by': filter_by,
        })


def album_update_view(request, album_id):
    if not request.user.is_authenticated:
        return redirect('music:register')
    else:
        obj = get_object_or_404(Album, pk=album_id)
        form = AlbumForm(request.POST or None, request.FILES or None, instance=obj)
        context = {'form': form}
        if form.is_valid():
            obj = form.save(commit=False)
            obj.set_websites()
            obj.save()
            messages.success(request, "Album info updated")
            return render(request, 'music/detail.html', {'album': obj})
        return render(request, 'music/album_update.html', context)
