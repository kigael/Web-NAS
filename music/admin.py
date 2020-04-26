# -*- coding: utf-8 -*-
from django.contrib import admin
from music.models import *

# Register your models here.
class MusicInline(admin.StackedInline):
	model = Music
	extra = 2

class MusicAlbumAdmin(admin.ModelAdmin):
	inlines = [MusicInline]
	list_display = ('name', 'description')

class MusicAdmin(admin.ModelAdmin):
	list_display = ('title', 'upload_date')

admin.site.register(MusicAlbum, MusicAlbumAdmin)
admin.site.register(Music, MusicAdmin)

