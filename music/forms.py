from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django import forms
from .models import Album, Song


class UserRegForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1',  'password2']


class AlbumForm(forms.ModelForm):
    class Meta:
        model = Album
        fields = ['artist', 'album_title', 'genre', 'facebook', 'album_logo']


class SongForm(forms.ModelForm):
    class Meta:
        model = Song
        fields = ['song_title', 'audio_file']
