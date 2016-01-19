# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('newshub', '0025_auto_20160118_0104'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='follow_endorse_page_seen',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='profile',
            name='tag_page_seen',
            field=models.BooleanField(default=False),
        ),
    ]
