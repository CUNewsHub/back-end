
from django.conf.urls import url


urlpatterns = [
    url(r'^$', 'newshub.views.home', name='home'),
    url(r'^top-stories/$', 'newshub.views.top_stories', name='top_stories'),
    url(r'^history/$', 'newshub.views.history', name='history'),
    url(r'^login/$', 'newshub.views.login', name='login'),
    url(r'^logout/$', 'newshub.views.logout', name='logout'),
    url(r'^profile/$', 'newshub.views.profile', name='profile'),
    url(r'^profile/(?P<pk>[0-9]+)/$', 'newshub.views.profile', name='profile'),
    url(
        r'view/article/(?P<action_type>history|home|top-stories)/(?P<pk>[0-9]+)/$',
        'newshub.views.view_article',
        name='view_article'),
    url(
        r'^article/add/comment/$',
        'newshub.views.add_comment', name='add_comment'),
    url(
        r'^new/article/$',
        'newshub.views.new_article',
        name='new_article'),
    url(
        r'^edit/article/(?P<pk>[0-9]+)/$',
        'newshub.views.edit_article',
        name='edit_article'),
    url(
        r'^action/(?P<action_type>follow|endorse|like)/$',
        'newshub.views.action',
        name='action'),
    url(
        r'^update/profile/(?P<pk>[0-9]+)/$',
        'newshub.views.update_profile',
        name='update_profile')
    # url(
    #     r'^my/articles/$',
    #     'newshub.views.author_articles',
    #     name='my_articles')

]
