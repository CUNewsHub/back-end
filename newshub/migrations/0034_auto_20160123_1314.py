# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('newshub', '0033_article_featured'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='follow_endorse_page_seen',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='society',
            name='follow_endorse_page_seen',
            field=models.BooleanField(default=True),
        ),
    ]
