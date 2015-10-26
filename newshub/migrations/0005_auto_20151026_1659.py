# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('newshub', '0004_auto_20151023_1050'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='category',
            options={'verbose_name_plural': 'Categories'},
        ),
        migrations.AddField(
            model_name='article',
            name='time_changed',
            field=models.DateTimeField(default=datetime.datetime(2015, 10, 26, 16, 59, 8, 827049), auto_now=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='article',
            name='time_uploaded',
            field=models.DateTimeField(default=datetime.datetime(2015, 10, 26, 16, 59, 16, 798742), auto_now_add=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='profile',
            name='crsid',
            field=models.CharField(max_length=7, null=True, blank=True),
        ),
    ]
