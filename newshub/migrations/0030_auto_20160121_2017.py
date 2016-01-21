# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('newshub', '0029_auto_20160121_1959'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userfeedback',
            name='feedback',
        ),
        migrations.AddField(
            model_name='userfeedback',
            name='feedback',
            field=models.ManyToManyField(to='newshub.Feedback'),
        ),
    ]
