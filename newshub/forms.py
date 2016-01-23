from django import forms
from .models import Article, Profile, Comment, Poll, Choice, Society, Tag
from redactor.widgets import RedactorEditor
from django_select2.forms import ModelSelect2TagWidget, Select2MultipleWidget
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from django.db.models import Count


# class TagWidget(ModelSelect2TagWidget):
#     search_fields = [
#         'name__icontains',
#     ]

#     queryset = Tag.objects.all()

#     def value_from_datadict(self, data, files, name):
#         values = super(TagWidget, self).value_from_datadict(data, files, name)
#         qs = self.queryset.filter(**{'pk__in': list(values)})
#         pks = set(force_text(getattr(o, 'pk')) for o in qs)
#         cleaned_values = []
#         for val in values:
#             if force_text(val) not in pks:
#                 val = self.queryset.create(name=val).pk
#             cleaned_values.append(val)
#         return cleaned_values
class TitleSearchFieldMixin(object):
    search_fields = [
        'name__icontains'
    ]


class TagWidget(TitleSearchFieldMixin, ModelSelect2TagWidget):
    model = Tag

    def create_value(self, value):
        self.get_queryset().create(name=value)


class NewArticleForm(forms.ModelForm):
    poll = forms.CharField(
        required=False,
        label='Add a poll',
        help_text="If you want to create a poll for this article, type a question here")

    class Meta:
        model = Article
        fields = [
            'title', 'header_picture', 'headline', 'content', 'poll', 'tags']
        exclude = ['author', 'likes', 'published']
        widgets = {
            'content': RedactorEditor(
                redactor_options={'buttons': [
                    'formatting', 'bold', 'italic', 'deleted',
                    'list', 'link', 'horizontalrule', 'orderedlist',
                    'unorderedlist']}),
            'tags': Select2MultipleWidget
        }

        help_texts = {
            'title': 'Maxmimum 60 characters',
            'headline': 'Maximum 360 characters'
        }


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        exclude = ['user', 'crsid_is_verified', 'tag_page_seen', 
                   'follow_endorse_page_seen']
        fields = ['display_name', 'picture', 'crsid', 'college', 'subject',
                  'year', 'about']
        help_texts = {
            'display_name': 'This name will be displayed as your' +
                            ' name everywhere on te website'
        }


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
    first_name = forms.CharField(
        label='Society Name', max_length=30, required=True)
    email = forms.EmailField(
        label='Society contact email', required=True)

    class Meta:
        model = User
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
        exclude = ('user', 'admins', 'tag_page_seen',
                   'follow_endorse_page_seen')
        help_texts = {
            'facebook_link': 'The official facebook page of the society, if exists',
            'website': 'The website of the society. Start with http://'
        }


class UpdateSocietyForm(SocietyDataForm):
    email = forms.EmailField()
    socname = forms.CharField(
        max_length=30, required=True, label='Society name')


class LandingTagsForm(forms.Form):
    LANDING_SET = [
        "Finance",
        "ISIS",
        "Austerity",
        "Development",
        "EU",
        "Refugees",
        "Economics",
        "Feminism",
        "Free Speech",
        "Football",
        "Rugby",
        "Food",
        "Theatre",
        "Conservatives",
        "Labour",
        "Cindies",
        "CUSU",
        "Film",
        "Careers",
        "Medicine",
        "Science"]

    tag_set = Tag.objects.all().filter(approved=True).filter(
        name__in=LANDING_SET)

    CHOICES = [(x.id, x) for x in tag_set]

    tags = forms.MultipleChoiceField(
        required=False,
        widget=forms.CheckboxSelectMultiple, choices=CHOICES)


class TagForm(forms.ModelForm):
    class Meta:
        model = Tag
        exclude = ('user_set', 'approved')


class SocietyLoginForm(AuthenticationForm):
    username = forms.CharField(max_length=254, label='Society ID')
