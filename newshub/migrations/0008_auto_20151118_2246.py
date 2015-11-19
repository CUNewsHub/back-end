# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('newshub', '0007_auto_20151118_2144'),
    ]

    operations = [
        migrations.CreateModel(
            name='Follow',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('author', models.ForeignKey(to='newshub.Author')),
                ('followed_by', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.RenameField(
            model_name='endorsement',
            old_name='endorsed_user',
            new_name='endorsed_by',
        ),
        migrations.AddField(
            model_name='article',
            name='likes',
            field=models.ManyToManyField(related_name='liked_articles', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='article',
            name='author',
            field=models.ForeignKey(to='newshub.Author'),
        ),
        migrations.AddField(
            model_name='author',
            name='followed_by',
            field=models.ManyToManyField(related_name='followed_author', null=True, through='newshub.Follow', to=settings.AUTH_USER_MODEL, blank=True),
        ),
    ]
