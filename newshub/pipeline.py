from requests import request, HTTPError
from django.core.files.base import ContentFile
from .models import Profile, Author


def create_profile(
        backend, user, response, details,
        is_new=False, *args, **kwargs):

    url = 'http://graph.facebook.com/{0}/picture?width=250&height=250'.format(response['id'])

    if is_new:
        try:
            response = request('GET', url, params={'type': 'large'})
            response.raise_for_status()
        except HTTPError:
            pass
        else:
            display_name = user.first_name+' '+user.last_name
            profile = Profile(user=user, display_name=display_name)
            profile.picture.save(
                '{0}_social.jpg'.format(user.username),
                ContentFile(response.content))
            profile.save()


def create_author(
    strategy, user, response, details,
        is_new=False, *args, **kwargs):

    if is_new:
        Author.objects.create(user=user)
