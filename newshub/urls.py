from django.views.generic import TemplateView
from django.conf.urls import url, include


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
        name='update_profile'),
    url(
        r'^update/society/(?P<pk>[0-9]+)/$',
        'newshub.views.update_society',
        name='update_society'),
    url(
        r'^article/add/poll/$',
        'newshub.views.article_add_poll',
        name='article_add_poll'),
    url(
        r'^article/edit/poll/(?P<pk>[0-9]+)/$',
        'newshub.views.article_edit_poll',
        name='article_edit_poll'),
    url(
        r'^article/delete/poll/(?P<pk>[0-9]+)/$',
        'newshub.views.article_delete_poll',
        name='article_delete_poll'),
    url(
        r'^article/poll/add/choice/$',
        'newshub.views.article_poll_add_choice',
        name='article_poll_add_choice'),
    url(
        r'^article/delete/poll/choice/(?P<pk>[0-9]+)/$',
        'newshub.views.article_delete_poll_choice',
        name='article_delete_poll_choice'),
    url(
        r'^article/poll/(?P<pk>[0-9]+)/vote/$',
        'newshub.views.article_poll_vote',
        name='article_poll_vote'),
    url(
        r'^article/(?P<a_id>[0-9]+)/add/feedback/(?P<f_id>[0-9]+)/$',
        'newshub.views.article_add_feedback',
        name='article_add_feedback'),
    url(
        r'^create/society/$',
        'newshub.views.create_society',
        name='create_society'),
    url(
        r'^societies/login/(?P<pk>[0-9]+)/$',
        'newshub.views.societies_login',
        name='societies_login'),

    # url(
    #     r'^my/articles/$',
    #     'newshub.views.author_articles',
    #     name='my_articles'),
    url(
        r'^tags/(?P<tag_name>[a-zA-Z]+)/$',
        'newshub.views.articles_by_tags',
        name='article_by_tags'),
    url(
        r'^society/login/$',
        'newshub.views.society_login',
        name='society_login'),
    url(
        r'^DB3B5A40DB893FA110A8EEAF41/$',
        TemplateView.as_view(template_name='newshub/tmp_login.html')),
    url(
        r'^landing/pages/tags/$',
        'newshub.views.landing_pages_tags',
        name='landing_pages_tags'),
    url(
        r'^landing/pages/follow/endorse/$',
        'newshub.views.landing_pages_follow_endorse',
        name='landing_pages_follow_endorse'),
    url(
        r'^privacy/policy/$',
        TemplateView.as_view(
            template_name='newshub/management/privacy_policy.html'),
        name='privacy_policy'),
    url(
        r'^about/us/$',
        TemplateView.as_view(
            template_name='newshub/management/about_us.html'),
        name='about_us'),
    url(
        r'^contact/us/$',
        TemplateView.as_view(
            template_name='newshub/management/contact_us.html'),
        name='contact_us'),
    url(
        r'^add/tag/$',
        'newshub.views.add_tag',
        name='add_tag')
]
