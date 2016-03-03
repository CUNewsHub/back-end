"""Context processors for newshub application."""
from django.conf import settings
from .models import Article


def testing_processor(request):
    """Test context processor."""
    if settings.DEBUG:
        article = Article.objects.all()[0]
        return {'article': article}
