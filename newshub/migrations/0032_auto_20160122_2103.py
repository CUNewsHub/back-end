# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('newshub', '0031_auto_20160122_1622'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tag',
            name='category',
            field=models.ForeignKey(default=1, to='newshub.Category'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='tag',
            name='name',
            field=models.CharField(unique=True, max_length=63),
        ),
    ]
