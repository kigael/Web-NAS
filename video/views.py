# -*- coding: utf-8 -*-
import os
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
from django.views.generic import ListView, DetailView
from video.models import VideoAlbum, Video

from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.core.urlresolvers import reverse_lazy
from mysite.views import LoginRequiredMixin
from django.shortcuts import get_object_or_404

import sys
reload(sys)
sys.setdefaultencoding("utf-8")
# Create your views here.
class AlbumLV(ListView):
	model = VideoAlbum

class AlbumDV(DetailView):
	model = VideoAlbum

class VideoDV(DetailView):
	model = Video

class VideoCreateView(LoginRequiredMixin, CreateView):
	model = Video
	fields = ['album', 'title', 'video']
	success_url = reverse_lazy('video:index')

	def form_valid(self, form):
		form.instance.owner = self.request.user
		return super(VideoCreateView, self).form_valid(form)

class VideoChangeLV(LoginRequiredMixin, ListView):
	model = Video
	template_name = 'video/video_change_list.html'

	def get_queryset(self):
		return Video.objects.filter(owner=self.request.user)

class VideoUpdateView(LoginRequiredMixin, UpdateView):
	model = Video
	fields = ['album', 'title', 'video']
	success_url = reverse_lazy('video:index')
	
class VideoDeleteView(LoginRequiredMixin, DeleteView):
	model = Video
	success_url = reverse_lazy('video:index')

class AlbumChangeLV(LoginRequiredMixin, ListView):
	template_name = 'video/album_change_list.html'

	def get_queryset(self):
		return VideoAlbum.objects.filter(owner=self.request.user)

class AlbumDeleteView(LoginRequiredMixin, DeleteView):
	model = VideoAlbum
	success_url = reverse_lazy('video:index')

from django.shortcuts import redirect
from video.forms import VideoInlineFormSet

class AlbumVideoCV(LoginRequiredMixin, CreateView):
	model = VideoAlbum
	fields = ['name', 'description']
	template_name = 'video/album_form.html'

	def get_context_data(self, **kwargs):
		context = super(AlbumVideoCV, self).get_context_data(**kwargs)
		if self.request.POST:
			context['formset'] = VideoInlineFormSet(self.request.POST, self.request.FILES)
		else:
			context['formset'] = VideoInlineFormSet()
		return context
	
	def form_valid(self, form):
		form.instance.owner = self.request.user
		context = self.get_context_data()
		formset = context['formset']
		for videoform in formset:
			videoform.instance.owner = self.request.user
		if formset.is_valid():
			self.object = form.save()
			formset.instance = self.object
			formset.save()
			return redirect(self.object.get_absolute_url())
		else:
			return self.render_to_response(self.get_context_data(form=form))

class AlbumVideoUV(LoginRequiredMixin, UpdateView):
	model = VideoAlbum
	fields = ['name', 'description']
	template_name = 'video/album_form.html'
	
	def get_context_data(self, **kwargs):
		context = super(AlbumVideoUV, self).get_context_data(**kwargs)
		if self.request.POST:
			context['formset'] = VideoInlineFormSet(self.request.POST, self.request.FILES, instance=self.object)
		else:
			context['formset'] = VideoInlineFormSet(instance=self.object)
		return context
	
	def form_valid(self, form):
		context = self.get_context_data()
		formset = context['formset']
		if formset.is_valid():
			self.object = form.save()
			formset.instance = self.object
			formset.save()
			return redirect(self.object.get_absolute_url())
		else:
			return self.render_to_response(self.get_context_data(form=form))
