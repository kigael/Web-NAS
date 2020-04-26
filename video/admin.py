# -*- coding: utf-8 -*-
from django.contrib import admin
from video.models import *

# Register your models here.
class VideoInline(admin.StackedInline):
	model = Video
	extra = 2

class VideoAlbumAdmin(admin.ModelAdmin):
	inlines = [VideoInline]
	list_display = ('name', 'description')

class VideoAdmin(admin.ModelAdmin):
	list_display = ('title', 'upload_date')

admin.site.register(VideoAlbum, VideoAlbumAdmin)
admin.site.register(Video, VideoAdmin)

