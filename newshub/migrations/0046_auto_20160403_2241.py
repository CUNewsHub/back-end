# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import redactor.fields


class Migration(migrations.Migration):

    dependencies = [
        ('newshub', '0045_auto_20160215_1424'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='content',
            field=redactor.fields.RedactorField(null=True, verbose_name=b'Body', blank=True),
        ),
        migrations.AlterField(
            model_name='article',
            name='tags',
            field=models.ManyToManyField(to='newshub.Tag', blank=True),
        ),
        migrations.AlterField(
            model_name='profile',
            name='picture',
            field=models.ImageField(default=b'profile_pictures/defaultpp.png', upload_to=b'profile_pictures/%Y/%m/%d'),
        ),
    ]
