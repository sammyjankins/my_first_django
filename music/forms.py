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
        fields = ['artist',
                  'album_title',
                  'genre',
                  'website_1',
                  'website_2',
                  'website_3',
                  'website_4',
                  'website_5',
                  'description',
                  'album_logo']


class SongForm(forms.Form):
    model = Song
    audio_files = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True}))

