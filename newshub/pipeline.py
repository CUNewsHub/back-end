from requests import request, HTTPError
from django.core.files.base import ContentFile
from .models import Profile


def create_profile(
        strategy, user, response, details,
        is_new=False, *args, **kwargs):

    url = 'http://graph.facebook.com/{0}/picture'.format(response['id'])

    if is_new:
        try:
            response = request('GET', url, params={'type': 'large'})
            response.raise_for_status()
        except HTTPError:
            pass
        else:
            profile = Profile(user=user)
            profile.picture.save(
                '{0}_social.jpg'.format(user.username),
                ContentFile(response.content))
            profile.save()
