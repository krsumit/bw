# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ChannelTags',
            fields=[
                ('tag_id', models.AutoField(serialize=False, primary_key=True)),
                ('tag_name', models.CharField(max_length=255)),
            ],
            options={
                'db_table': 'channel_tags',
                'managed': False,
            },
        ),
    ]
