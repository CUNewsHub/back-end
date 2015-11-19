# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('newshub', '0006_auto_20151118_2140'),
    ]

    operations = [
        migrations.AlterField(
            model_name='author',
            name='endorsed_by',
            field=models.ManyToManyField(related_name='endorsed_author', null=True, through='newshub.Endorsement', to=settings.AUTH_USER_MODEL, blank=True),
        ),
    ]
