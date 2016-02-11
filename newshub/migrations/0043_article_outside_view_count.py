# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('newshub', '0042_auto_20160209_1737'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='outside_view_count',
            field=models.IntegerField(default=0),
        ),
    ]
