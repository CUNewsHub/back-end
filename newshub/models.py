from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.OneToOneField(User)
    picture = models.ImageField(upload_to='profile_pictures/%Y/%m/%d')
    about = models.TextField(blank=True, null=True)


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
    author = models.ForeignKey(User)
    title = models.CharField(max_length=255)
    headline = models.TextField()
    content = models.TextField()
    published = models.BooleanField(default=False)
    tags = models.ManyToManyField(Tag)
