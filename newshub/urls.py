
from django.conf.urls import url


urlpatterns = [
    url(r'^$', 'newshub.views.home', name='home'),
    url(r'^login/$', 'newshub.views.login', name='login'),
    url(r'^logout/$', 'newshub.views.logout', name='logout'),
]
