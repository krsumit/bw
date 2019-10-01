# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('quickbytes', '0002_auto_20150820_0848'),
    ]

    operations = [
        migrations.AlterModelTable(
            name='quickbytes',
            table='quickBytes',
        ),
        migrations.AlterModelTable(
            name='quickbytesphotos',
            table='quickBytesPhotos',
        ),
        migrations.AlterModelTable(
            name='quickbytestags',
            table='quickBytesTags',
        ),
        migrations.AlterModelTable(
            name='quickbytestopic',
            table='quickBytesTopic',
        ),
    ]
