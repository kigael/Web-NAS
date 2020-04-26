from django.conf.urls import url	
from video.views import *

urlpatterns = [
	url(r'^$', AlbumLV.as_view(), name='index'),
	url(r'^album/$', AlbumLV.as_view(), name='album_list'),
	url(r'^album/(?P<pk>\d+)$', AlbumDV.as_view(), name='album_detail'),
	url(r'^video/(?P<pk>\d+)$', VideoDV.as_view(), name='video_detail'),

	url(r'^album/add/$', AlbumVideoCV.as_view(), name='album_add'),
	url(r'^album/change/$', AlbumChangeLV.as_view(), name='album_change'),
	url(r'^album/(?P<pk>[0-9]+)/update/$', AlbumVideoUV.as_view(), name='album_update'),
	url(r'^album/(?P<pk>[0-9]+)/delete/$', AlbumDeleteView.as_view(), name='album_delete'),

	url(r'^video/add/$', VideoCreateView.as_view(), name='video_add'),
	url(r'^video/change/$',VideoChangeLV.as_view(), name='video_change'),
	url(r'^video/(?P<pk>[0-9]+)/update/$', VideoUpdateView.as_view(), name='video_update'),
	url(r'^video/(?P<pk>[0-9]+)/delete/$', VideoDeleteView.as_view(), name='video_delete'),
]
