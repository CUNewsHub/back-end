# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('newshub', '0027_auto_20160119_1403'),
    ]

    operations = [
        migrations.AddField(
            model_name='tag',
            name='user_set',
            field=models.ManyToManyField(to=settings.AUTH_USER_MODEL),
        ),
    ]
