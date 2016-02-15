# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('newshub', '0043_article_outside_view_count'),
    ]

    operations = [
        migrations.CreateModel(
            name='EmailNotification',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('weekly_newsletter', models.BooleanField(default=True, verbose_name=b'Receive a weekly newsletter about new articles')),
                ('article_liked', models.BooleanField(default=False, verbose_name=b'Receive a notification whenever your article is liked')),
                ('comment', models.BooleanField(default=True, verbose_name=b'Receive a notification whenever your article has anew comment, or your comment has a new reply.')),
                ('followed_author_new_article', models.BooleanField(default=True, verbose_name=b'Receive a notification when an author you followed has posted a new article')),
                ('user', models.OneToOneField(related_name='email_notifications', to='newshub.Profile')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
