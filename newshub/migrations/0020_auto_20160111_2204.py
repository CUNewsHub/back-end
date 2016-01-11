# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('newshub', '0019_auto_20160109_1906'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='year',
            field=models.CharField(blank=True, max_length=10, null=True, choices=[(b'IA', b'First Year'), (b'IB', b'Second Year'), (b'II', b'Third Year'), (b'III', b'Fourth Year'), (b'M+', b'Masters'), (b'GRAD', b'Graduate'), (b'N/A', b'N/A')]),
        ),
        migrations.AlterUniqueTogether(
            name='userfeedback',
            unique_together=set([('article', 'user')]),
        ),
    ]
