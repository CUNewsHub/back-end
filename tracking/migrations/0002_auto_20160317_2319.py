# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('newshub', '0045_auto_20160215_1424'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('tracking', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='PageVisitor',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('logged_in_user', models.BooleanField()),
                ('visited_time', models.DateTimeField(auto_now_add=True)),
                ('session_key', models.CharField(unique=True, max_length=40)),
            ],
        ),
        migrations.CreateModel(
            name='ArticleVisitor',
            fields=[
                ('pagevisitor_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='tracking.PageVisitor')),
                ('obj', models.ForeignKey(to='newshub.Article')),
            ],
            bases=('tracking.pagevisitor',),
        ),
        migrations.CreateModel(
            name='CategoryVisitor',
            fields=[
                ('pagevisitor_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='tracking.PageVisitor')),
                ('obj', models.ForeignKey(to='newshub.Category')),
            ],
            bases=('tracking.pagevisitor',),
        ),
        migrations.CreateModel(
            name='LoginPageVisitor',
            fields=[
                ('pagevisitor_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='tracking.PageVisitor')),
            ],
            bases=('tracking.pagevisitor',),
        ),
        migrations.CreateModel(
            name='NewsFeedVisitor',
            fields=[
                ('pagevisitor_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='tracking.PageVisitor')),
                ('newsfeed_type', models.CharField(max_length=32, choices=[(b'history', b'history'), (b'top-stories', b'top-stories'), (b'personal-feed', b'personal-feed')])),
            ],
            bases=('tracking.pagevisitor',),
        ),
        migrations.CreateModel(
            name='ProfileVisitor',
            fields=[
                ('pagevisitor_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='tracking.PageVisitor')),
                ('obj', models.ForeignKey(to='newshub.Profile')),
            ],
            bases=('tracking.pagevisitor',),
        ),
        migrations.CreateModel(
            name='SocietyVisitor',
            fields=[
                ('pagevisitor_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='tracking.PageVisitor')),
                ('obj', models.ForeignKey(to='newshub.Society')),
            ],
            bases=('tracking.pagevisitor',),
        ),
        migrations.CreateModel(
            name='TagVisitor',
            fields=[
                ('pagevisitor_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='tracking.PageVisitor')),
                ('obj', models.ForeignKey(to='newshub.Tag')),
            ],
            bases=('tracking.pagevisitor',),
        ),
        migrations.AddField(
            model_name='pagevisitor',
            name='user',
            field=models.ForeignKey(blank=True, to=settings.AUTH_USER_MODEL, null=True),
        ),
    ]
