
from django.conf.urls import url


urlpatterns = [
    url(r'^$', 'newshub.views.home', name='home')
]
