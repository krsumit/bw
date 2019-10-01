# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='QuickBytes',
            fields=[
                ('quick_byte_id', models.AutoField(serialize=False, primary_key=True)),
                ('quick_byte_author_type', models.IntegerField()),
                ('quick_byte_author_id', models.IntegerField()),
                ('quick_byte_title', models.TextField()),
                ('quick_byte_description', models.TextField()),
                ('quick_byte_sponsered', models.IntegerField()),
                ('quick_byte_published_date', models.DateTimeField()),
            ],
            options={
                'db_table': 'quick_bytes',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='QuickBytesPhotos',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('quick_byte_id', models.IntegerField()),
                ('quick_byte_photo_name', models.CharField(max_length=100)),
                ('quick_byte_photo_url', models.TextField()),
                ('quick_byte_photo_description', models.TextField()),
            ],
            options={
                'db_table': 'quick_bytes_photos',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='QuickBytesTags',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('quick_byte_id', models.IntegerField()),
                ('tag_id', models.IntegerField()),
            ],
            options={
                'db_table': 'quick_bytes_tags',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='QuickBytesTopic',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('quick_byte_id', models.IntegerField()),
                ('topic_id', models.IntegerField()),
            ],
            options={
                'db_table': 'quick_bytes_topic',
                'managed': False,
            },
        ),
    ]
