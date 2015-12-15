# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('newshub', '0013_auto_20151215_1313'),
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('text', models.TextField()),
                ('made_time', models.DateTimeField(auto_now=True)),
                ('article', models.ForeignKey(to='newshub.Article')),
                ('made_by', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
