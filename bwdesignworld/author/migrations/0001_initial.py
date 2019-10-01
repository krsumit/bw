# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Author',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('author_id', models.IntegerField()),
                ('author_name', models.CharField(max_length=255)),
                ('author_photo', models.CharField(max_length=255)),
                ('author_bio', models.TextField()),
                ('author_type', models.IntegerField()),
                ('column_id', models.IntegerField()),
            ],
            options={
                'db_table': 'author',
                'managed': False,
            },
        ),
    ]
