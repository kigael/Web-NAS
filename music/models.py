# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.utils.encoding import python_2_unicode_compatible
from django.db import models
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User

from django.db.models.signals import post_delete, pre_save
from django.dispatch import receiver
# Create your models here.

@python_2_unicode_compatible
class MusicAlbum(models.Model):
	name = models.CharField(max_length=50)
	description = models.CharField('One Line Description', max_length=100, blank=True)
	owner = models.ForeignKey(User, null=True)

	class Meta:
		ordering = ['name']

	def __str__(self):
		return self.name
	
	def get_absolute_url(self):
		return reverse('music:album_detail', args=(self.id,))

@python_2_unicode_compatible
class Music(models.Model):
	album = models.ForeignKey(MusicAlbum)
	title = models.CharField(max_length=50)
	music = models.FileField(upload_to='music/%Y/%m')
	description = models.TextField('Music Description', blank=True)
	upload_date = models.DateTimeField('Upload Date', auto_now_add=True)
	owner = models.ForeignKey(User, null=True)

	class Meta:
		ordering = ['title']

	def __str__(self):
		return self.title
	
	def get_absolute_url(self):
		return reverse('music:music_detail', args=(self.id,))

import os
@receiver(post_delete, sender=Music)
def submission_delete(sender, instance, **kwargs):
	instance.music.delete(False)

@receiver(pre_save, sender=Music)
def auto_delete_file_on_change(sender, instance, **kwargs):
	if not instance.pk:
		return False
	try:
		old_file = Music.objects.get(pk=instance.pk).music
	except Music.DoesNotExist:
		return False
	new_file = instance.music
	if not old_file == new_file:
		if os.path.isfile(old_file.path):
			os.remove(old_file.path)
