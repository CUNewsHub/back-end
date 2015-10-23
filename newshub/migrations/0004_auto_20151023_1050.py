# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('newshub', '0003_article_published'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='tag',
            name='article',
        ),
        migrations.AddField(
            model_name='article',
            name='tags',
            field=models.ManyToManyField(to='newshub.Tag'),
        ),
    ]
