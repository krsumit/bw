# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ChannelTopics',
            fields=[
                ('topic_id', models.AutoField(serialize=False, primary_key=True)),
                ('topic_name', models.CharField(max_length=255)),
                ('topic_url', models.CharField(max_length=255)),
                ('category_id', models.IntegerField()),
            ],
            options={
                'db_table': 'channel_topics',
                'managed': False,
            },
        ),
    ]
