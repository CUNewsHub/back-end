# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tracking', '0002_auto_20160317_2319'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pagevisitor',
            name='session_key',
            field=models.CharField(max_length=40),
        ),
    ]
