from music.models import MusicAlbum, Music
from django.forms.models import inlineformset_factory

MusicInlineFormSet = inlineformset_factory(MusicAlbum, Music, fields = ['music', 'title', 'description'], extra = 10)
