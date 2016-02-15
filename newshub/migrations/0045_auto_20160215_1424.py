# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('newshub', '0044_emailnotification'),
    ]

    operations = [
        migrations.RenameField(
            model_name='emailnotification',
            old_name='user',
            new_name='profile',
        ),
    ]
