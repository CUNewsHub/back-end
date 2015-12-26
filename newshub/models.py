from django.db import models
from django.contrib.auth.models import User


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


class Profile(models.Model):
    YEAR_CHOICES = (
        ('IA', 'IA'),
        ('IB', 'IB'),
        ('II', 'II'),
        ('III', 'III'),
        ('MPhil', 'Mphil'),
        ('MA', 'MA'),
        ('MEng', 'MEng'),
        ('MMath', 'MMath'),
        ('PhD', 'PhD'),
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


class Endorsement(models.Model):
    author = models.ForeignKey(Author)
    endorsed_by = models.ForeignKey(User)


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
    category = models.ForeignKey(Category)

    def __unicode__(self):
        return self.name


class Article(models.Model):
    author = models.ForeignKey(Author)
    title = models.CharField(max_length=255)
    headline = models.TextField(verbose_name='Subheading')
    content = models.TextField(verbose_name='Article Body')
    published = models.BooleanField(default=False)
    tags = models.ManyToManyField(Tag)
    time_uploaded = models.DateTimeField(auto_now_add=True)
    time_changed = models.DateTimeField(auto_now=True)
    likes = models.ManyToManyField(
        User, related_name='liked_articles', blank=True)
    header_picture = models.ImageField(
        upload_to='article_header_pictures/%Y/%m/%d')


class ViewedArticles(models.Model):
    user = models.ForeignKey(User)
    article = models.ForeignKey(Article)
    viewed_time = models.DateTimeField(auto_now=True)


class Comment(models.Model):
    made_by = models.ForeignKey(User)
    article = models.ForeignKey(Article)
    text = models.TextField(verbose_name='New Comment')
    made_time = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-made_time']
