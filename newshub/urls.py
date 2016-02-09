from django.views.generic import TemplateView
from django.conf.urls import url


urlpatterns = [
    url(r'^personal-feed/$', 'newshub.views.home', name='home'),
    url(r'^top-stories/$', 'newshub.views.top_stories', name='top_stories'),
    url(r'^history/$', 'newshub.views.history', name='history'),
    url(r'^$', 'newshub.views.login', name='login'),
    url(r'^logout/$', 'newshub.views.logout', name='logout'),
    url(r'^profile/$', 'newshub.views.profile', name='self_profile'),
    url(r'^profile/(?P<pk>[0-9]+)/$', 'newshub.views.profile', name='profile'),
    url(
        (r'view/article/(?P<action_type>[\w\W]+)' +
         '/(?P<pk>[0-9a-z\-]+)/$'),
        'newshub.views.view_article',
        name='view_article'),
    url(
        r'view/article/(?P<pk>[0-9a-z\-]+)/$',
        'newshub.views.view_article_outside',
        name='view_article_outside'),
    url(
        r'^article/add/comment/$',
        'newshub.views.add_comment', name='add_comment'),
    url(
        r'^article/make/featured/$',
        'newshub.views.article_make_featured',
        name='article_make_featured'),
    url(
        r'^new/article/$',
        'newshub.views.new_article',
        name='new_article'),
    url(
        r'^edit/article/(?P<pk>[0-9a-z\-]+)/$',
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
        r'^tags/(?P<tag_name>[\w|\W]+)/$',
        'newshub.views.articles_by_tags',
        name='article_by_tags'),
    # url(
    #     r'^society/login/$',
    #     'newshub.views.society_login',
    #     name='society_login'),
    # url(r'^user/email/login/$',
    #     'newshub.views.user_email_login',
    #     name='user_email_login'),
    # url(
    #    r'^DB3B5A40DB893FA110A8EEAF41/$',
    #    TemplateView.as_view(template_name='newshub/tmp_login.html')),
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
        name='add_tag'),
    url(r'^delete/comment/$',
        'newshub.views.delete_comment',
        name='delete_comment'),
    url(r'^edit/comment/$',
        'newshub.views.edit_comment',
        name='edit_comment'),
    url(r'^society/change/password/$',
        'newshub.views.society_change_password',
        name='society_change_password'),
    url(r'^society/change/password/confirmation/$',
        TemplateView.as_view(
            template_name='newshub/society_change_password_confirmation.html'),
        name='society_change_password_confirmation'),
    url(r'^category/(?P<category>[\w\W]+)/$',
        'newshub.views.articles_by_category',
        name='articles_by_category'),
    url(r'^register/$',
        'newshub.views.register',
        name='register')
]
