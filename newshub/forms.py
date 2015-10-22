from django import forms
from .models import Article


class NewArticleForm(forms.ModelForm):
    published = forms.BooleanField(
        label='Publish?',
        required=False)

    class Meta:
        model = Article
        exclude = ['author']
