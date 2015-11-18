from django import forms
from .models import Article
from redactor.widgets import RedactorEditor
from django_select2.forms import ModelSelect2MultipleWidget

class TagWidget(ModelSelect2MultipleWidget):
    search_fields = [
        'name__icontains'
        ]

class NewArticleForm(forms.ModelForm):
    published = forms.BooleanField(
        label='Publish?',
        required=False)

    class Meta:
        model = Article
        exclude = ['author']
        widgets = {
            'content': RedactorEditor(
                allow_image_upload=False,
                allow_file_upload=False),
            'tags': TagWidget
        }
