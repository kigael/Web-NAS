from django.conf.urls import url	
from music.views import *

urlpatterns = [
	url(r'^$', AlbumLV.as_view(), name='index'),
	url(r'^album/$', AlbumLV.as_view(), name='album_list'),
	url(r'^album/(?P<pk>\d+)$', AlbumDV.as_view(), name='album_detail'),
	url(r'^music/(?P<pk>\d+)$', MusicDV.as_view(), name='music_detail'),

	url(r'^album/add/$', AlbumMusicCV.as_view(), name='album_add'),
	url(r'^album/change/$', AlbumChangeLV.as_view(), name='album_change'),
	url(r'^album/(?P<pk>[0-9]+)/update/$', AlbumMusicUV.as_view(), name='album_update'),
	url(r'^album/(?P<pk>[0-9]+)/delete/$', AlbumDeleteView.as_view(), name='album_delete'),

	url(r'^music/add/$', MusicCreateView.as_view(), name='music_add'),
	url(r'^music/change/$',MusicChangeLV.as_view(), name='music_change'),
	url(r'^music/(?P<pk>[0-9]+)/update/$', MusicUpdateView.as_view(), name='music_update'),
	url(r'^music/(?P<pk>[0-9]+)/delete/$', MusicDeleteView.as_view(), name='music_delete'),
]
