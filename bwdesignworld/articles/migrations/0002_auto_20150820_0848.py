# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='articleauthor',
            options={'managed': True},
        ),
        migrations.AlterModelOptions(
            name='articlecategory',
            options={'managed': True},
        ),
        migrations.AlterModelOptions(
            name='articleimages',
            options={'managed': True},
        ),
        migrations.AlterModelOptions(
            name='articles',
            options={'managed': True},
        ),
        migrations.AlterModelOptions(
            name='articletags',
            options={'managed': True},
        ),
        migrations.AlterModelOptions(
            name='articletopics',
            options={'managed': True},
        ),
        migrations.AlterModelOptions(
            name='articlevideo',
            options={'managed': True},
        ),
        migrations.AlterModelOptions(
            name='articleview',
            options={'managed': True},
        ),
    ]
