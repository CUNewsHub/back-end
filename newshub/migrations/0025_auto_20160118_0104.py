# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('newshub', '0024_auto_20160118_0028'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tag',
            name='category',
            field=models.ForeignKey(blank=True, to='newshub.Category', null=True),
        ),
    ]
