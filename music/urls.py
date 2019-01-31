from django.conf.urls import url
from django.contrib.auth import views as av
from . import views

app_name = 'music'

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^register/$', views.register, name='register'),
    url(r'^login/$', av.LoginView.as_view(template_name='music/login.html'), name='login'),
    url(r'^logout/$', av.LogoutView.as_view(template_name='music/logout.html'), name='logout'),
    url(r'^(?P<album_id>[0-9]+)/$', views.detail, name='detail'),
    url(r'^create_album/$', views.create_album, name='create_album'),
    url(r'^(?P<album_id>[0-9]+)/create_song/$', views.create_song, name='create_song'),
    url(r'^(?P<album_id>[0-9]+)/delete_album/$', views.delete_album, name='delete_album'),
    url(r'album/(?P<pk>[0-9]+)/$', views.AlbumUpdate.as_view(), name='album-update'),
    url(r'^(?P<album_id>[0-9]+)/favorite_album/$', views.favorite_album, name='favorite_album'),

]
