# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='OutsideArticleVisitor',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('session_key', models.CharField(unique=True, max_length=40)),
                ('ip_address', models.CharField(max_length=20, null=True, blank=True)),
                ('user_agent', models.CharField(max_length=255, null=True, blank=True)),
                ('entry_point', models.CharField(max_length=255, null=True, blank=True)),
                ('session_start', models.DateTimeField(auto_now_add=True)),
                ('logged_in', models.BooleanField(default=False)),
                ('login_time', models.DateTimeField(null=True, blank=True)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
