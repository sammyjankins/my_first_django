from django.conf.urls import url
from django.contrib.auth import views as av
from django.urls import reverse_lazy, path, include

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
    url(r'^(?P<album_id>[0-9]+)/delete_song/(?P<song_id>[0-9]+)/$', views.delete_song, name='delete_song'),
    url(r'album/(?P<pk>[0-9]+)/$', views.AlbumUpdate.as_view(), name='album-update'),
    url(r'^(?P<album_id>[0-9]+)/favorite_album/$', views.favorite_album, name='favorite_album'),
    url(r'^(?P<song_id>[0-9]+)/favorite/$', views.favorite, name='favorite'),
    url(r'^songs/(?P<filter_by>[a-zA_Z]+)/$', views.songs, name='songs'),
    url(r'^password-reset/$',
        av.PasswordResetView.as_view(email_template_name='music/password_reset_email.html',
                                     success_url=reverse_lazy('music:password_reset_done'),
                                     template_name='music/password_reset.html'), name='password_reset'),
    url(r'^password-reset/done/$',
        av.PasswordResetDoneView.as_view(template_name='music/password_reset_done.html'), name='password_reset_done'),
    url(r'^password-reset-confirm/(?P<uidb64>[\w-]+)/(?P<token>[\w-]+)/$',
        av.PasswordResetConfirmView.as_view(success_url=reverse_lazy('music:password_reset_complete'),
                                            template_name='music/password_reset_confirm.html'),
        name='password_reset_confirm'),
    url(r'^password-reset/complete/$',
        av.PasswordResetCompleteView.as_view(template_name='music/password_reset_complete.html'),
        name='password_reset_complete'),
]
