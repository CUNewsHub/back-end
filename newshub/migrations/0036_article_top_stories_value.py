# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('newshub', '0035_article_z'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='top_stories_value',
            field=models.FloatField(default=15.0),
        ),
    ]
