from django.http import Http404, HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from .models import Society, Profile


def landing_pages_seen(original_function):
    def landing_pages_check(request, *args, **kwargs):
        try:
            profile = request.user.profile
        except Profile.DoesNotExist:
            try:
                profile = request.user.society
            except Society.DoesNotExist:
                raise Http404

        if not profile.tag_page_seen and not profile.follow_endorse_page_seen:
            return HttpResponseRedirect(reverse('newshub:landing_pages_tags'))
        elif not profile.tag_page_seen:
            return HttpResponseRedirect(reverse('newshub:landing_pages_tags'))
        elif not profile.follow_endorse_page_seen:
            return HttpResponseRedirect(reverse(
                'newshub:landing_pages_follow_endorse'))
        else:
            return original_function(request, *args, **kwargs)

    return landing_pages_check
