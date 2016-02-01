from django.db import models
# from django.contrib.auth.models import User
# Create your models here.


class SimpleVisiorMixin(models.Model):
    session_key = models.CharField(max_length=40, unique=True)
    ip_address = models.CharField(max_length=20, null=True, blank=True)
    user_agent = models.CharField(max_length=255, null=True, blank=True)
    entry_point = models.CharField(max_length=255, null=True, blank=True)
    session_start = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True

    def __unicode__(self):
        return self.session_key


class OutsideArticleVisitor(SimpleVisiorMixin):
    logged_in = models.BooleanField(default=False)
    login_time = models.DateTimeField(null=True, blank=True)
