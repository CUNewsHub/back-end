# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('newshub', '0028_tag_user_set'),
    ]

    operations = [
        migrations.RenameField(
            model_name='viewedarticles',
            old_name='viewed_time',
            new_name='last_viewed_time',
        ),
        migrations.AddField(
            model_name='viewedarticles',
            name='number_of_views',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='article',
            name='header_picture',
            field=models.ImageField(null=True, upload_to=b'article_header_pictures/%Y/%m/%d', blank=True),
        ),
        migrations.AlterField(
            model_name='article',
            name='headline',
            field=models.TextField(null=True, verbose_name=b'Subheading', blank=True),
        ),
        migrations.AlterField(
            model_name='poll',
            name='title',
            field=models.CharField(max_length=255, verbose_name=b'Poll question'),
        ),
        migrations.AlterField(
            model_name='society',
            name='logo',
            field=models.ImageField(default='', upload_to=b'society_pictures/%Y/%m/%d'),
            preserve_default=False,
        ),
    ]
