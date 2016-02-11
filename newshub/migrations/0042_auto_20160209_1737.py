# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import redactor.fields


class Migration(migrations.Migration):

    dependencies = [
        ('newshub', '0041_article_url_text'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='content',
            field=redactor.fields.RedactorField(verbose_name=b'Body'),
        ),
    ]
