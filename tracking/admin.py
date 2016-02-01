from django.contrib import admin
from .models import OutsideArticleVisitor


class OutsideArticleVisitorAdmin(admin.ModelAdmin):
    list_display = ('session_key', 'ip_address', 'entry_point',
                    'session_start', 'login_time', 'logged_in')
    list_filter = ('logged_in',)
    fields = ()

admin.site.register(OutsideArticleVisitor, OutsideArticleVisitorAdmin)
