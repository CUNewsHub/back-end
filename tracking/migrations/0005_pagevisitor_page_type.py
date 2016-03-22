# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tracking', '0004_trackingmetadata'),
    ]

    operations = [
        migrations.AddField(
            model_name='pagevisitor',
            name='page_type',
            field=models.CharField(default='', max_length=32),
            preserve_default=False,
        ),
    ]
