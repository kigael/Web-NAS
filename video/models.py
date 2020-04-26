# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.utils.encoding import python_2_unicode_compatible
from django.db import models
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User

from django.db.models.signals import post_delete, pre_save
from django.dispatch import receiver

import sys
reload(sys)
sys.setdefaultencoding("utf-8")
# Create your models here.

@python_2_unicode_compatible
class VideoAlbum(models.Model):
	name = models.CharField(max_length=50)
	description = models.CharField('One Line Description', max_length=100, blank=True)
	owner = models.ForeignKey(User, null=True)

	class Meta:
		ordering = ['name']

	def __str__(self):
		return self.name
	
	def get_absolute_url(self):
		return reverse('video:album_detail', args=(self.id,))

@python_2_unicode_compatible
class Video(models.Model):
	album = models.ForeignKey(VideoAlbum)
	title = models.CharField(max_length=50)
	video = models.FileField(upload_to='video/%Y/%m')
	description = models.TextField('Video Description', blank=True)
	upload_date = models.DateTimeField('Upload Date', auto_now_add=True)
	owner = models.ForeignKey(User, null=True)

	class Meta:
		ordering = ['title']

	def __str__(self):
		return self.title
	
	def get_absolute_url(self):
		return reverse('video:video_detail', args=(self.id,))

import os
@receiver(post_delete, sender=Video)
def submission_delete(sender, instance, **kwargs):
	instance.video.delete(False)

@receiver(pre_save, sender=Video)
def auto_delete_file_on_change(sender, instance, **kwargs):
	if not instance.pk:
		return False
	try:
		old_file = Video.objects.get(pk=instance.pk).video
	except Video.DoesNotExist:
		return False
	new_file = instance.video
	if not old_file == new_file:
		if os.path.isfile(old_file.path):
			os.remove(old_file.path)
