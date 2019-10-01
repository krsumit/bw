# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ChannelCategory',
            fields=[
                ('category_id', models.AutoField(serialize=False, primary_key=True)),
                ('category_name', models.CharField(max_length=255)),
                ('category_parent', models.IntegerField()),
            ],
            options={
                'db_table': 'channel_category',
                'managed': False,
            },
        ),
    ]
