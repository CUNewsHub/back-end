# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('newshub', '0030_auto_20160121_2017'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='content',
            field=models.TextField(verbose_name=b'Body'),
        ),
        migrations.AlterField(
            model_name='article',
            name='headline',
            field=models.TextField(max_length=360, null=True, verbose_name=b'Subtitle', blank=True),
        ),
        migrations.AlterField(
            model_name='article',
            name='title',
            field=models.CharField(max_length=60),
        ),
    ]
