# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('newshub', '0023_auto_20160117_2034'),
    ]

    operations = [
        migrations.AddField(
            model_name='tag',
            name='approved',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='society',
            name='logo',
            field=models.ImageField(null=True, upload_to=b'society_pictures/%Y/%m/%d', blank=True),
        ),
    ]
