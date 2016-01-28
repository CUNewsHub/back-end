# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('newshub', '0038_auto_20160124_1553'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='tag_page_seen',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='society',
            name='tag_page_seen',
            field=models.BooleanField(default=True),
        ),
    ]
