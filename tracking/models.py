"""Models for tracking app."""

from django.db import models
from django.contrib.auth.models import User
from model_utils.managers import InheritanceManager
from newshub.models import Article, Profile, Category, Tag, Society
# from django.contrib.auth.models import User
# Create your models here.


class SimpleVisiorMixin(models.Model):
    """SimpleVisiorMixin class."""

    session_key = models.CharField(max_length=40, unique=True)
    ip_address = models.CharField(max_length=20, null=True, blank=True)
    user_agent = models.CharField(max_length=255, null=True, blank=True)
    entry_point = models.CharField(max_length=255, null=True, blank=True)
    session_start = models.DateTimeField(auto_now_add=True)

    class Meta:
        """Meta class for SimpleVisiorMixin."""

        abstract = True

    def __unicode__(self):
        """Unicode function."""
        return self.session_key


class OutsideArticleVisitor(SimpleVisiorMixin):
    """OutsideArticleVisitor object."""

    logged_in = models.BooleanField(default=False)
    login_time = models.DateTimeField(null=True, blank=True)


class PageVisitor(models.Model):
    """Page visitor parent class."""

    logged_in_user = models.BooleanField()
    visited_time = models.DateTimeField(auto_now_add=True)
    session_key = models.CharField(max_length=40)
    user = models.ForeignKey(User, blank=True, null=True)

    objects = InheritanceManager()

    @staticmethod
    def create_page_visitor(page_type, request, obj=None, **kwargs):
        """Static method for creating PageVisitor classes."""
        page_visitor = None
        kwargs = kwargs

        if request.user.is_authenticated():
            kwargs['logged_in_user'] = True
            kwargs['user'] = request.user
        else:
            kwargs['logged_in_user'] = False
            kwargs['user'] = None

        kwargs['session_key'] = request.session.session_key

        if page_type == 'article':
            page_visitor = ArticleVisitor
        elif page_type == 'profile':
            page_visitor = ProfileVisitor
        elif page_type == 'society':
            page_visitor = SocietyVisitor
        elif page_type == 'category':
            page_visitor = CategoryVisitor
        elif page_type == 'newsfeed':
            page_visitor = NewsFeedVisitor
        elif page_type == 'login_page':
            page_visitor = LoginPageVisitor
        elif page_type == 'tag':
            page_visitor = TagVisitor

        if obj is not None:
            page_visitor.objects.create(obj=obj, **kwargs)
        else:
            page_visitor.objects.create(**kwargs)


class ArticleVisitor(PageVisitor):
    """Article visitor class."""

    obj = models.ForeignKey(Article)


class ProfileVisitor(PageVisitor):
    """Profile visitor class."""

    obj = models.ForeignKey(Profile)


class SocietyVisitor(PageVisitor):
    """SocietyVisitor class."""

    obj = models.ForeignKey(Society)


class NewsFeedVisitor(PageVisitor):
    """Docstring for NewsFeedVisitor."""

    HISTORY = 'history'
    TOP_STORIES = 'top-stories'
    PERSONAL_FEED = 'personal-feed'

    NEWSFEED_CHOICES = [
        (HISTORY, HISTORY),
        (TOP_STORIES, TOP_STORIES),
        (PERSONAL_FEED, PERSONAL_FEED)
    ]

    newsfeed_type = models.CharField(max_length=32, choices=NEWSFEED_CHOICES)


class CategoryVisitor(PageVisitor):
    """CategoryVisitor class."""

    obj = models.ForeignKey(Category)


class TagVisitor(PageVisitor):
    """TagVisitor class."""

    obj = models.ForeignKey(Tag)


class LoginPageVisitor(PageVisitor):
    """LoginPageVisitor class."""

    pass
