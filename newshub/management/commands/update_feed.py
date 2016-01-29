# from ...models import Article
import math
import pytz
import datetime
from newshub.views import _get_redis_instance as gri
from django.core.management.base import BaseCommand
from newshub.models import Profile, Article
from django.db.models import Q
from newshub.feed import initialise_category_vector
from newshub.feed import get_occurrence_category_vector
from newshub import models
from django.contrib.auth.models import User


def _time_decay_function(seconds):
    if seconds < 3600:
        return 3.5
    elif seconds <= 2592000:
        return -0.5 * math.log(seconds / 3.6e6)
    else:
        return 0.16


def _calculate_article_value(article):
    viewed_set = article.viewedarticles_set.filter(
        ~Q(user=article.author.user))
    views = sum([x.number_of_views for x in viewed_set])
    likes = 20 * article.likes.count()
    comments = 30 * article.comment_set.count()
    society_factor = 1
    try:
        article.author.user.profile
    except Profile.DoesNotExist:
        society_factor = 1

    dt = datetime.datetime.now(pytz.utc) - article.time_uploaded

    time_factor = _time_decay_function(int(dt.total_seconds()))

    z_value = article.z

    value = (views + likes + comments) * society_factor * time_factor + z_value

    return float(value)


def _update_articles():
    for article in Article.objects.filter(published=True):
        article_value = _calculate_article_value(article)
        article.top_stories_value = article_value
        article.save()

    print "Ran _update_articles() for top-stories"


def _update_user_feed(redis, user):
    if redis is None:
        return
    try:
        user_category_vector = eval(
            redis.get('category_vector_' + str(user.pk)))
    except TypeError:
        initialise_category_vector(redis, user, models)
        user_category_vector = eval(
            redis.get('category_vector_' + str(user.pk)))

    article_set = []

    dot_product = 0.0
    for article in Article.objects.filter(published=True):
        occ_category_vector = get_occurrence_category_vector(article, models)

        for k in occ_category_vector:
            dot_product += occ_category_vector[k] * user_category_vector[k]

        article_set.append(
            (dot_product * article.top_stories_value, article.pk))

    article_set.sort()

    redis.delete('personalised_feed_' + str(user.pk))
    if article_set != []:
        redis.lpush(
            'personalised_feed_' + str(user.pk), *[x[1] for x in article_set])


def _update_feed():
    r = gri()
    for user in User.objects.all():
        _update_user_feed(r, user)

    del r
    print "Updated feed()"


class Command(BaseCommand):
    help = 'Updating top-stories feed, and storing it in Redis'

    def handle(self, *args, **options):
        _update_articles()
        _update_feed()
