from video.models import VideoAlbum, Video
from django.forms.models import inlineformset_factory

VideoInlineFormSet = inlineformset_factory(VideoAlbum, Video, fields = ['video', 'title', 'description'], extra = 10)
