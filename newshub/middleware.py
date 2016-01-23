from social.apps.django_app.middleware import SocialAuthExceptionMiddleware
from django.http import HttpResponseRedirect
from social.exceptions import AuthAlreadyAssociated
from django.contrib.auth import logout


class NewshubSocialAuthMiddleware(SocialAuthExceptionMiddleware):
    def process_exception(self, request, exception):
        if isinstance(exception, AuthAlreadyAssociated):
            logout(request)
            return HttpResponseRedirect('/')
        else:
            raise exception
