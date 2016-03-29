from social.apps.django_app.middleware import SocialAuthExceptionMiddleware
from django.http import HttpResponseRedirect, HttpResponse
from social.exceptions import AuthAlreadyAssociated
from django.contrib.auth import logout


class NewshubSocialAuthMiddleware(SocialAuthExceptionMiddleware):
    def process_exception(self, request, exception):
        if isinstance(exception, AuthAlreadyAssociated):
            logout(request)
            return HttpResponseRedirect('/')
        else:
            raise exception


class LoggedInUserPreProcessingMiddleware(object):
    def process_request(self, request):
        if not request.user.is_authenticated():
            return
        else:
            if request.user.email == '':
                return HttpResponse('aaasd')
