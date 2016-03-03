from django.dispatch import Signal, receiver
from .models import Article, Profile
from mailer import send_html_mail
from django.template.loader import get_template
from django.template import Context

new_article = Signal()
article_liked = Signal()


def send_notification_mail(
        recipient_list, subject, template, data,
        sender_address='Cambridge NewsHub <no-reply@camnewshub.com>'):
    sender = sender_address
    subject = subject
    text_content = get_template(
        'newshub/notifications/txt/' + template + '.txt')
    html_content = get_template(
        'newshub/notifications/html/' + template + '.html')

    d = Context(data)

    text_content = text_content.render(d)
    html_content = html_content.render(d)

    send_html_mail(subject, text_content, html_content, sender, recipient_list)


@receiver(new_article, sender=Article)
def author_new_article_receiver(sender, **kwargs):
    article = kwargs['article']
    for user in article.author.followed_by.all():
        try:
            profile = user.profile
            if profile.email_notifications.followed_author_new_article:
                send_notification_mail(
                    recipient_list=[user.email],
                    subject='Cambridge NewsHub: New article posted by %s' % (
                        article.author,),
                    template='new_article',
                    data={
                        'user': user,
                        'article': article
                    }
                )
        except Profile.DoesNotExist:
            pass
