from django.db import models
from django.contrib.auth.models import User
from django.core.validators import RegexValidator


class College(models.Model):
    name = models.CharField(max_length=63)

    def __unicode__(self):
        return self.name


class Course(models.Model):
    name = models.CharField(max_length=127)

    def __unicode__(self):
        return self.name


class Subject(models.Model):
    name = models.CharField(max_length=127)

    def __unicode__(self):
        return self.name


class LandingPages(models.Model):
    tag_page_seen = models.BooleanField(default=False)
    follow_endorse_page_seen = models.BooleanField(default=False)

    class Meta:
        abstract = True


class Profile(LandingPages):
    YEAR_CHOICES = (
        ('IA', 'First Year'),
        ('IB', 'Second Year'),
        ('II', 'Third Year'),
        ('III', 'Fourth Year'),
        ('M+', 'Masters'),
        ('GRAD', 'Graduate'),
        ('N/A', 'N/A'),
    )

    user = models.OneToOneField(User)
    picture = models.ImageField(upload_to='profile_pictures/%Y/%m/%d')
    about = models.TextField(blank=True, null=True)
    crsid = models.CharField(blank=True, null=True, max_length=7)
    crsid_is_verified = models.BooleanField(default=False)
    display_name = models.CharField(max_length=127)
    college = models.ForeignKey(College, blank=True, null=True)
    subject = models.ForeignKey(Subject, blank=True, null=True)
    year = models.CharField(choices=YEAR_CHOICES, blank=True, null=True,
                            max_length=10)


class Society(LandingPages):
    user = models.OneToOneField(User)
    admins = models.ManyToManyField(User, related_name='admin_of')
    logo = models.ImageField(upload_to='society_pictures/%Y/%m/%d')
    facebook_link = models.URLField(
        blank=True, null=True, validators=[RegexValidator(
            regex='^https?://www\.facebook\.com',
            message='invalid facebook page')])
    website = models.URLField(blank=True, null=True)
    about = models.TextField(blank=True, null=True)


class Author(models.Model):
    user = models.OneToOneField(User)
    endorsed_by = models.ManyToManyField(
        User, through='Endorsement',
        related_name='endorsed_author', blank=True)
    followed_by = models.ManyToManyField(
        User, through='Follow',
        related_name='followed_author',
        blank=True)

    def is_verified(self):
        return self.user.profile.crsid_is_verified


class TooManyEndorsementsError(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)


class Endorsement(models.Model):
    author = models.ForeignKey(Author)
    endorsed_by = models.ForeignKey(User)

    def save(self, *args, **kwargs):
        if self.endorsed_by.endorsement_set.count() > 4:
            raise TooManyEndorsementsError(
                'You have reached the limit on the Endorsenents, which is 3.')
        else:
            super(Endorsement, self).save(*args, **kwargs)


class Follow(models.Model):
    author = models.ForeignKey(Author)
    followed_by = models.ForeignKey(User)


class Category(models.Model):
    name = models.CharField(max_length=63)

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name_plural = u'Categories'


class Tag(models.Model):
    name = models.CharField(max_length=63)
    category = models.ForeignKey(Category, null=True, blank=True)
    approved = models.BooleanField(default=False)
    user_set = models.ManyToManyField(User)

    def __unicode__(self):
        return self.name


class Article(models.Model):
    author = models.ForeignKey(Author)
    title = models.CharField(max_length=60)
    headline = models.TextField(
        verbose_name='Subtitle', max_length=360, blank=True, null=True)
    content = models.TextField(verbose_name='Body')
    published = models.BooleanField(default=False)
    tags = models.ManyToManyField(Tag)
    time_uploaded = models.DateTimeField(auto_now_add=True)
    time_changed = models.DateTimeField(auto_now=True)
    likes = models.ManyToManyField(
        User, related_name='liked_articles', blank=True)
    header_picture = models.ImageField(
        upload_to='article_header_pictures/%Y/%m/%d',
        blank=True, null=True)

    def __unicode__(self):
        return self.title


class ViewedArticles(models.Model):
    user = models.ForeignKey(User)
    article = models.ForeignKey(Article)
    last_viewed_time = models.DateTimeField(auto_now=True)
    number_of_views = models.IntegerField(default=0)


class Comment(models.Model):
    made_by = models.ForeignKey(User)
    article = models.ForeignKey(Article)
    text = models.TextField(verbose_name='New Comment')
    made_time = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-made_time']


class Poll(models.Model):
    title = models.CharField(max_length=255, verbose_name='Poll question')
    voted = models.ManyToManyField(User)
    article = models.OneToOneField(Article, null=True, blank=True)

    def __unicode__(self):
        return self.title


class Choice(models.Model):
    poll = models.ForeignKey(Poll)
    choice_text = models.CharField(max_length=255)
    votes = models.IntegerField(default=0)

    def __unicode__(self):
        return self.choice_text

    class Meta:
        ordering = ['choice_text']


class Feedback(models.Model):
    name = models.CharField(max_length=255)

    def __unicode__(self):
        return self.name


class UserFeedback(models.Model):
    article = models.ForeignKey(Article, related_name='user_feedback')
    user = models.ForeignKey(User)
    feedback = models.ManyToManyField(Feedback)

    class Meta:
        unique_together = ('article', 'user')
