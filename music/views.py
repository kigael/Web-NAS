from django.views.generic import ListView, DetailView
from music.models import MusicAlbum, Music

from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.core.urlresolvers import reverse_lazy
from mysite.views import LoginRequiredMixin

# Create your views here.
class AlbumLV(ListView):
	model = MusicAlbum

class AlbumDV(DetailView):
	model = MusicAlbum

class MusicDV(DetailView):
	model = Music

class MusicCreateView(LoginRequiredMixin, CreateView):
	model = Music
	fields = ['album', 'title', 'music']
	success_url = reverse_lazy('music:index')

	def form_valid(self, form):
		form.instance.owner = self.request.user
		return super(MusicCreateView, self).form_valid(form)

class MusicChangeLV(LoginRequiredMixin, ListView):
	model = Music
	template_name = 'music/music_change_list.html'

	def get_queryset(self):
		return Music.objects.filter(owner=self.request.user)

class MusicUpdateView(LoginRequiredMixin, UpdateView):
	model = Music
	fields = ['album', 'title', 'music']
	success_url = reverse_lazy('music:index')
	
class MusicDeleteView(LoginRequiredMixin, DeleteView):
	model = Music
	success_url = reverse_lazy('music:index')

class AlbumChangeLV(LoginRequiredMixin, ListView):
	template_name = 'music/album_change_list.html'

	def get_queryset(self):
		return MusicAlbum.objects.filter(owner=self.request.user)

class AlbumDeleteView(LoginRequiredMixin, DeleteView):
	model = MusicAlbum
	success_url = reverse_lazy('music:index')

from django.shortcuts import redirect
from music.forms import MusicInlineFormSet

class AlbumMusicCV(LoginRequiredMixin, CreateView):
	model = MusicAlbum
	fields = ['name', 'description']
	template_name = 'music/album_form.html'

	def get_context_data(self, **kwargs):
		context = super(AlbumMusicCV, self).get_context_data(**kwargs)
		if self.request.POST:
			context['formset'] = MusicInlineFormSet(self.request.POST, self.request.FILES)
		else:
			context['formset'] = MusicInlineFormSet()
		return context
	
	def form_valid(self, form):
		form.instance.owner = self.request.user
		context = self.get_context_data()
		formset = context['formset']
		for musicform in formset:
			musicform.instance.owner = self.request.user
		if formset.is_valid():
			self.object = form.save()
			formset.instance = self.object
			formset.save()
			return redirect(self.object.get_absolute_url())
		else:
			return self.render_to_response(self.get_context_data(form=form))

class AlbumMusicUV(LoginRequiredMixin, UpdateView):
	model = MusicAlbum
	fields = ['name', 'description']
	template_name = 'music/album_form.html'
	
	def get_context_data(self, **kwargs):
		context = super(AlbumMusicUV, self).get_context_data(**kwargs)
		if self.request.POST:
			context['formset'] = MusicInlineFormSet(self.request.POST, self.request.FILES, instance=self.object)
		else:
			context['formset'] = MusicInlineFormSet(instance=self.object)
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
