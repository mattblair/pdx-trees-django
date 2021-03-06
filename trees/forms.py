from django import forms

from .models import SupplementalContent

class SupplementalContentForm(forms.ModelForm):
    class Meta:
        model = SupplementalContent
        fields = [
            'title', 'subtitle',
            'summary', 'article_text',
            'credit', 'copyright_notice',
            
            'photo', 'photo_title',
            'photo_caption', 'photo_credit',
            'photo_copyright',
            
            'audio', 'audio_title',
            'audio_caption', 'audio_transcription',
            'audio_credit', 'audio_copyright'
        ]