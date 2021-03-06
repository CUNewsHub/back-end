import re
from django.db import models
from django.db.models import Count
from django.contrib.auth.models import User
from django.core.validators import RegexValidator
from redactor.fields import RedactorField


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
    tag_page_seen = models.BooleanField(default=True)
    follow_endorse_page_seen = models.BooleanField(default=True)

    class Meta:
        abstract = True


class Profile(LandingPages):
    YEAR_CHOICES = (
        ('IA', 'First Year'),
        ('IB', 'Second Year'),
        ('II', 'Third Year'),
        ('III', 'Fourth Year'),
        ('M+', 'Masters'),
        ('PostGrad', 'Postgraduate'),
        ('GRAD', 'Graduate'),
        ('N/A', 'N/A'),
    )

    user = models.OneToOneField(User)
    picture = models.ImageField(
        default="profile_pictures/defaultpp.png",
        upload_to='profile_pictures/%Y/%m/%d')
    about = models.TextField(blank=True, null=True)
    crsid = models.CharField(blank=True, null=True, max_length=7)
    crsid_is_verified = models.BooleanField(default=False)
    display_name = models.CharField(max_length=127)
    college = models.ForeignKey(College, blank=True, null=True)
    subject = models.ForeignKey(Subject, blank=True, null=True)
    year = models.CharField(choices=YEAR_CHOICES, blank=True, null=True,
                            max_length=10)

    def save(self, *args, **kwargs):
        super(Profile, self).save(*args, **kwargs)

        EmailNotification.objects.get_or_create(profile=self)

    def __unicode__(self):
        return "%s %s" % (self.user.first_name, self.user.last_name)


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

    def __unicode__(self):
        return "%s%s" % (self.user.first_name, self.user.last_name)


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

    def __unicode__(self):
        return self.user.first_name + " " + self.user.last_name


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
    name = models.CharField(max_length=63, unique=True)
    category = models.ForeignKey(Category)
    approved = models.BooleanField(default=False)
    user_set = models.ManyToManyField(User, blank=True)

    def __unicode__(self):
        return self.name


class Article(models.Model):
    author = models.ForeignKey(Author)
    title = models.CharField(max_length=60)
    headline = models.TextField(
        verbose_name='Subtitle', max_length=360, blank=True, null=True)
    content = RedactorField(
        verbose_name='Body',
        redactor_options={'buttons': [
            'formatting', 'bold', 'italic', 'deleted',
            'list', 'link', 'horizontalrule', 'orderedlist',
            'unorderedlist', 'image', 'fontsize']},
        allow_file_upload=True,
        allow_image_upload=True,
        blank=True,
        null=True)
    published = models.BooleanField(default=False)
    tags = models.ManyToManyField(Tag, blank=True)
    time_uploaded = models.DateTimeField(auto_now_add=True)
    time_changed = models.DateTimeField(auto_now=True)
    likes = models.ManyToManyField(
        User, related_name='liked_articles', blank=True)
    header_picture = models.ImageField(
        upload_to='article_header_pictures/%Y/%m/%d',
        blank=True, null=True)
    featured = models.BooleanField(default=False)
    z = models.IntegerField(default=1)
    top_stories_value = models.FloatField(default=15.0)
    url_text = models.CharField(
        max_length=60, unique=True, null=True, blank=True)
    outside_view_count = models.IntegerField(default=0)

    def __unicode__(self):
        return self.title

    def generate_url_text(self):
        url_text = self.title.lower()
        # sub several spaces to one
        url_text = re.sub(r'[\ ]+', ' ', url_text)
        url_text = re.sub(r'[^0-9a-z\ ]+', '', url_text)
        url_text = url_text.replace(' ', '-')

        number = Article.objects.filter(url_text__startswith=url_text).count()

        url_text += str(number)

        return url_text

    def save(self, *args, **kwargs):
        super(Article, self).save(*args, **kwargs)
        self.url_text = self.generate_url_text()

    def get_distinct_view_count(self):
        return ViewedArticles.objects.filter(article=self).count()

    def get_total_view_count(self):
        total_inside_views = sum([
            x.number_of_views for x in ViewedArticles.objects.filter(
                article=self)
        ])

        return total_inside_views + self.outside_view_count

    def get_feedback_set(self):
        return Feedback.objects.all()\
            .filter(userfeedback__article=self)\
            .annotate(f_count=Count('userfeedback'))\
            .order_by('-f_count', 'name')

    def save(self, *args, **kwargs):
        if self.author.article_set.filter(featured=True).count() < 3:
            self.featured = True
        super(Article, self).save(*args, **kwargs)


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


class NotificationMixin(models.Model):
    weekly_newsletter = models.BooleanField(
        default=True,
        verbose_name='Receive a weekly newsletter about new articles')

    article_liked = models.BooleanField(
        default=False,
        verbose_name='Receive a notification whenever your article is liked')

    comment = models.BooleanField(
        default=True,
        verbose_name=('Receive a notification whenever your article has a' +
                      'new comment, or your comment has a new reply.'))

    followed_author_new_article = models.BooleanField(
        default=True,
        verbose_name=('Receive a notification when an author you followed ' +
                      'has posted a new article'))

    class Meta:
        abstract = True


class EmailNotification(NotificationMixin):
    profile = models.OneToOneField(Profile, related_name='email_notifications',
                                   unique=True)
