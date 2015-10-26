
from django.conf.urls import url


urlpatterns = [
    url(r'^$', 'newshub.views.home', name='home'),
    url(r'^login/$', 'newshub.views.login', name='login'),
    url(r'^logout/$', 'newshub.views.logout', name='logout'),
    url(r'^profile/$', 'newshub.views.profile', name='profile'),
    url(r'^profile/(?P<pk>[0-9]+)/$', 'newshub.views.profile', name='profile'),
    url(
        r'^view/article/(?P<pk>[0-9]+)/$',
        'newshub.views.view_article',
        name='view_article'),
    url(
        r'^new/article/$',
        'newshub.views.new_article',
        name='new_article'),
    url(
        r'^edit/article/(?P<pk>[0-9]+)/$',
        'newshub.views.edit_article',
        name='edit_article'),
    url(
        r'^my/articles/$',
        'newshub.views.author_articles',
        name='my_articles')

]
