# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('newshub', '0034_auto_20160123_1314'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='z',
            field=models.IntegerField(default=1),
        ),
    ]
