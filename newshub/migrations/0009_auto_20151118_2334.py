# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('newshub', '0008_auto_20151118_2246'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='likes',
            field=models.ManyToManyField(related_name='liked_articles', null=True, to=settings.AUTH_USER_MODEL, blank=True),
        ),
    ]
