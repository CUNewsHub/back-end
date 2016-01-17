# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('newshub', '0021_society'),
    ]

    operations = [
        migrations.RenameField(
            model_name='society',
            old_name='administrators',
            new_name='admins',
        ),
    ]
