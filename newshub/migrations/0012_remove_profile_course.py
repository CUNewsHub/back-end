# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('newshub', '0011_auto_20151214_2213'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='course',
        ),
    ]
