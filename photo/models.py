# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.utils.encoding import python_2_unicode_compatible

from django.db import models

from django.core.urlresolvers import reverse

from photo.fields import ThumbnailImageField

from django.contrib.auth.models import User

from django.db.models.signals import post_delete, pre_save
from django.dispatch import receiver
# Create your models here.

@python_2_unicode_compatible
class Album(models.Model):
	name = models.CharField(max_length=50)
	description = models.CharField('One Line Description', max_length=100, blank=True)
	owner = models.ForeignKey(User, null=True)

	class Meta:
		ordering = ['name']

	def __str__(self):
		return self.name
	
	def get_absolute_url(self):
		return reverse('photo:album_detail', args=(self.id,))

@python_2_unicode_compatible
class Photo(models.Model):
	album = models.ForeignKey(Album)
	title = models.CharField(max_length=50)
	image = ThumbnailImageField(upload_to='photo/%Y/%m')
	description = models.TextField('Photo Description', blank=True)
	upload_date = models.DateTimeField('Upload Date', auto_now_add=True)
	owner = models.ForeignKey(User, null=True)

	class Meta:
		ordering = ['title']

	def __str__(self):
		return self.title
	
	def get_absolute_url(self):
		return reverse('photo:photo_detail', args=(self.id,))

import os
@receiver(post_delete, sender=Photo)
def submission_delete(sender, instance, **kwargs):
	instance.image.delete(False)  

@receiver(pre_save, sender=Photo)
def auto_delete_file_on_change(sender, instance, **kwargs):
	if not instance.pk:
		return False
	try:
		old_file = Photo.objects.get(pk=instance.pk).image
	except Photo.DoesNotExist:
		return False	
	new_file = instance.image
	if not old_file == new_file:
		if os.path.isfile(old_file.path):
			 os.remove(old_file.path)
			 old_thumb_file = old_file.path.split('.')
			 old_thumb_file.insert(-1, 'thumb')
			 os.remove(".".join(old_thumb_file))
