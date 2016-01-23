# from ...models import Article
import math
import pytz
import datetime
from newshub.views import _get_redis_instance as gri
from django.core.management.base import BaseCommand
from newshub.models import Profile, Article


def _time_decay_function(seconds):
    if seconds < 3600:
        return 3.5
    elif seconds <= 2592000:
        return -0.5*math.log(seconds/3.6e6)
    else:
        return 0.16


def _calculate_article_value(article):
    views = sum([x.number_of_views for x in article.viewedarticles_set.all()])
    likes = 20*article.likes.count()
    comments = 30*article.comment_set.count()
    society_factor = 1
    try:
        article.author.user.profile
    except Profile.DoesNotExist:
        society_factor = 1.5

    dt = datetime.datetime.now(pytz.utc) - article.time_uploaded

    time_factor = _time_decay_function(int(dt.total_seconds()))

    z_value = article.z

    value = (views+likes+comments)*society_factor*time_factor + z_value

    return float(value)


class Command(BaseCommand):
    help = 'Updating top-stories feed, and storing it in Redis'

    def handle(self, *args, **options):
        r = gri()

        article_set = []

        for article in Article.objects.filter(published=True):
            article_value = _calculate_article_value(article)
            article_set.append((article_value, article.pk))

        # sorting low to high
        article_set.sort()
        # delete the top stories
        r.ltrim('top_stories', -1, 0)
        # lpush, so it will first push the low values
        r.lpush('top_stories', *[x[1] for x in article_set])

        print "Ran update tags"