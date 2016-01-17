# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('newshub', '0022_auto_20160112_1929'),
    ]

    operations = [
        migrations.AddField(
            model_name='society',
            name='about',
            field=models.TextField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='society',
            name='facebook_link',
            field=models.URLField(blank=True, null=True, validators=[django.core.validators.RegexValidator(regex=b'^https?://www\\.facebook\\.com', message=b'invalid facebook page')]),
        ),
        migrations.AddField(
            model_name='society',
            name='logo',
            field=models.ImageField(null=True, upload_to=b'profile_pictures/%Y/%m/%d', blank=True),
        ),
        migrations.AddField(
            model_name='society',
            name='website',
            field=models.URLField(null=True, blank=True),
        ),
    ]
