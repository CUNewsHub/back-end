import datetime
from django.conf import settings
from tracking.models import OutsideArticleVisitor
from tracking.utils import get_ip


class VisitorTrackingMiddleware(object):
    ARTICLE_VIEW_PREFIX = '/view/article/'
    LOGIN_PREFIX = '/login/facebook/'

    @property
    def prefixes(self):
        """Returns a list of URL prefixes that we should not track"""

        if not hasattr(self, '_prefixes'):
            self._prefixes = getattr(settings, 'NO_TRACKING_PREFIXES', [])

            if not getattr(settings, '_FREEZE_TRACKING_PREFIXES', False):
                for name in ('MEDIA_URL', 'STATIC_URL'):
                    url = getattr(settings, name)
                    if url and url != '/':
                        self._prefixes.append(url)

                        settings.NO_TRACKING_PREFIXES = self._prefixes
                        settings._FREEZE_TRACKING_PREFIXES = True

        return self._prefixes

    def process_request(self, request):
        # filtering authenticated users
        if request.user.is_authenticated():
            return

        # filtering static and media files
        for prefix in self.prefixes:
            if request.path.startswith(prefix):
                return

        ip_address = get_ip(request)
        user_agent = unicode(
            request.META.get('HTTP_USER_AGENT', '')[:255], errors='ignore')

        if not request.session.session_key:
            request.session.save()
        session_key = request.session.session_key

        if request.path.startswith(self.ARTICLE_VIEW_PREFIX):
            opv_list = OutsideArticleVisitor.objects.filter(
                ip_address=ip_address, user_agent=user_agent)
            if opv_list.count() == 1:
                opv = opv_list[0]
                opv.session_key = session_key
                opv.save()
            elif opv_list.count() == 0:
                opv, created = OutsideArticleVisitor.objects.get_or_create(
                    session_key=session_key)

                if created:
                    opv.entry_point = request.path
                    opv.user_agent = user_agent
                    opv.ip_address = ip_address
                    opv.save()
                    return
            else:
                opv = opv_list.order_by('-session_start')[0]
                opv.session_key = session_key
                opv.save()

                for duplicate in opv_list.order_by('-session_start')[1:]:
                    duplicate.delete()

        elif request.path.startswith(self.LOGIN_PREFIX):
            try:
                opv = OutsideArticleVisitor.objects.get(
                    session_key=session_key)
                opv.logged_in = True
                opv.login_time = datetime.datetime.now()
                opv.save()
                return

            except OutsideArticleVisitor.DoesNotExist:
                return
