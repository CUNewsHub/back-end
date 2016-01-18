from django import forms
from .models import Article, Profile, Comment, Poll, Choice, Society, Tag
from redactor.widgets import RedactorEditor
from django_select2.forms import ModelSelect2TagWidget
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.utils.encoding import force_text


class TagWidget(ModelSelect2TagWidget):
    search_fields = [
        'name__icontains',
    ]

    queryset = Tag.objects.all()

    def value_from_datadict(self, data, files, name):
        values = super(TagWidget, self).value_from_datadict(data, files, name)
        qs = self.queryset.filter(**{'name__in': list(values)})
        pks = set(force_text(getattr(o, 'name')) for o in qs)
        cleaned_values = []
        for val in values:
            if force_text(val) not in pks:
                val = self.queryset.create(name=val)
            cleaned_values.append(val)
        return cleaned_values


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
            'tags': TagWidget()
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
