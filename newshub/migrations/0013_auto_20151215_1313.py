# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('newshub', '0012_remove_profile_course'),
    ]

    operations = [
        migrations.CreateModel(
            name='ViewedArticles',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('viewed_time', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.AlterField(
            model_name='article',
            name='content',
            field=models.TextField(verbose_name=b'Article Body'),
        ),
        migrations.AlterField(
            model_name='article',
            name='headline',
            field=models.TextField(verbose_name=b'Subheading'),
        ),
        migrations.AddField(
            model_name='viewedarticles',
            name='article',
            field=models.ForeignKey(to='newshub.Article'),
        ),
        migrations.AddField(
            model_name='viewedarticles',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
        ),
    ]
