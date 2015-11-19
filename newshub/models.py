from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.OneToOneField(User)
    picture = models.ImageField(upload_to='profile_pictures/%Y/%m/%d')
    about = models.TextField(blank=True, null=True)
    crsid = models.CharField(blank=True, null=True, max_length=7)


class Author(models.Model):
    user = models.OneToOneField(User)
    endorsed_by = models.ManyToManyField(
        User, through='Endorsement',
        related_name='endorsed_author', blank=True,
        null=True)
    followed_by = models.ManyToManyField(
        User, through='Follow',
        related_name='followed_author',
        blank=True, null=True)


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
    headline = models.TextField()
    content = models.TextField()
    published = models.BooleanField(default=False)
    tags = models.ManyToManyField(Tag)
    time_uploaded = models.DateTimeField(auto_now_add=True)
    time_changed = models.DateTimeField(auto_now=True)
    likes = models.ManyToManyField(
        User, related_name='liked_articles', blank=True, null=True)
