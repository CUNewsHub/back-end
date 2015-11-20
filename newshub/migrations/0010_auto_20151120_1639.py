# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('newshub', '0009_auto_20151118_2334'),
    ]

    operations = [
        migrations.CreateModel(
            name='College',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=63)),
            ],
        ),
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=127)),
            ],
        ),
        migrations.AddField(
            model_name='profile',
            name='crsid_is_verified',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='profile',
            name='display_name',
            field=models.CharField(default='T', max_length=127),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='profile',
            name='college',
            field=models.ForeignKey(blank=True, to='newshub.College', null=True),
        ),
        migrations.AddField(
            model_name='profile',
            name='course',
            field=models.ForeignKey(blank=True, to='newshub.Course', null=True),
        ),
    ]
