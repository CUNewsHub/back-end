# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('newshub', '0015_auto_20151215_1639'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='header_picture',
            field=models.ImageField(default='', upload_to=b'article_header_pictures/%Y/%m/%d'),
            preserve_default=False,
        ),
    ]
