# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('newshub', '0026_auto_20160119_1353'),
    ]

    operations = [
        migrations.AddField(
            model_name='society',
            name='follow_endorse_page_seen',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='society',
            name='tag_page_seen',
            field=models.BooleanField(default=False),
        ),
    ]
