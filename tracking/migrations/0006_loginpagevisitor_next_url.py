# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tracking', '0005_pagevisitor_page_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='loginpagevisitor',
            name='next_url',
            field=models.CharField(max_length=255, null=True, blank=True),
        ),
    ]
