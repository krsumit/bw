# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('quickbytes', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='quickbytes',
            options={'managed': True},
        ),
        migrations.AlterModelOptions(
            name='quickbytesphotos',
            options={'managed': True},
        ),
        migrations.AlterModelOptions(
            name='quickbytestags',
            options={'managed': True},
        ),
        migrations.AlterModelOptions(
            name='quickbytestopic',
            options={'managed': True},
        ),
    ]
