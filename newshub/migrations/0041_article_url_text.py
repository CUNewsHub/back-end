# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('newshub', '0040_auto_20160128_1731'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='url_text',
            field=models.CharField(max_length=60, unique=True, null=True, blank=True),
        ),
    ]
