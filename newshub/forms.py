from django import forms
from .models import Article, Profile, Comment, Poll, Choice
from redactor.widgets import RedactorEditor
from django_select2.forms import ModelSelect2MultipleWidget


class TagWidget(ModelSelect2MultipleWidget):
    search_fields = [
        'name__icontains'
        ]


class NewArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        exclude = ['author', 'likes', 'published']
        widgets = {
            'content': RedactorEditor(
                redactor_options={'buttons': [
                    'formatting', 'bold', 'italic', 'deleted',
                    'list', 'link', 'horizontalrule', 'orderedlist',
                    'unorderedlist']}),
            'tags': TagWidget
        }


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        exclude = ['user', 'picture', 'crsid_is_verified']


class CommentForm(forms.ModelForm):
    class Meta:
        exclude = ['made_by', 'made_time']
        model = Comment
        widgets = {'article': forms.HiddenInput()}


class PollForm(forms.ModelForm):
    class Meta:
        model = Poll
        exclude = ['voted']
        widgets = {'article': forms.HiddenInput()}


class ChoiceForm(forms.ModelForm):
    class Meta:
        model = Choice
        fields = ['poll', 'choice_text']
        widgets = {'poll': forms.HiddenInput()}
