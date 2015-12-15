# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('newshub', '0010_auto_20151120_1639'),
    ]

    operations = [
        migrations.CreateModel(
            name='Subject',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=127)),
            ],
        ),
        migrations.AddField(
            model_name='profile',
            name='year',
            field=models.CharField(blank=True, max_length=10, null=True, choices=[(b'IA', b'IA'), (b'IB', b'IB'), (b'II', b'II'), (b'III', b'III'), (b'MPhil', b'Mphil'), (b'MA', b'MA'), (b'MEng', b'MEng'), (b'MMath', b'MMath'), (b'PhD', b'PhD'), (b'N/A', b'N/A')]),
        ),
        migrations.AlterField(
            model_name='article',
            name='likes',
            field=models.ManyToManyField(related_name='liked_articles', to=settings.AUTH_USER_MODEL, blank=True),
        ),
        migrations.AlterField(
            model_name='author',
            name='endorsed_by',
            field=models.ManyToManyField(related_name='endorsed_author', through='newshub.Endorsement', to=settings.AUTH_USER_MODEL, blank=True),
        ),
        migrations.AlterField(
            model_name='author',
            name='followed_by',
            field=models.ManyToManyField(related_name='followed_author', through='newshub.Follow', to=settings.AUTH_USER_MODEL, blank=True),
        ),
        migrations.AddField(
            model_name='profile',
            name='subject',
            field=models.ForeignKey(blank=True, to='newshub.Subject', null=True),
        ),
    ]
