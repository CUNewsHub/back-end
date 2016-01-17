from django import forms
from .models import Article, Profile, Comment, Poll, Choice, Society
from redactor.widgets import RedactorEditor
from django_select2.forms import ModelSelect2MultipleWidget
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class TagWidget(ModelSelect2MultipleWidget):
    search_fields = [
        'name__icontains'
        ]


class NewArticleForm(forms.ModelForm):
    poll = forms.CharField(
        required=False,
        label='Poll question',
        help_text="If you want to create a poll for this article, type a question here")

    class Meta:
        model = Article
        fields = [
            'title', 'header_picture', 'headline', 'content', 'tags', 'poll']
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
        exclude = ['user', 'crsid_is_verified']
        fields = ['display_name', 'picture', 'crsid', 'college', 'subject',
                  'year', 'about']


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


class SocietyForm(UserCreationForm):
    class Meta:
        model = User
        labels = {
            'first_name': 'Society Name',
            'email': 'Soceity contact email',
        }
        fields = ('first_name', 'email')

    def save(self, commit=True):
        user = super(SocietyForm, self).save(commit=False)
        user.first_name = self.cleaned_data['first_name']
        user.email = self.cleaned_data['email']

        if commit:
            user.save()

        return user


class SocietyDataForm(forms.ModelForm):
    class Meta:
        model = Society
        exclude = ('user', 'admins')


class UpdateSocietyForm(SocietyDataForm):
    email = forms.EmailField()
    socname = forms.CharField(max_length=30, required=True, label='Society name')
