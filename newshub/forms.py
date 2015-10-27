from django import forms
from .models import Article
from tinymce.widgets import TinyMCE


class NewArticleForm(forms.ModelForm):
    published = forms.BooleanField(
        label='Publish?',
        required=False)

    class Meta:
        model = Article
        exclude = ['author']
        widgets = {
            'content': TinyMCE()
        }
