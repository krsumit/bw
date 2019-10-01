# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0005_auto_20150820_0941'),
    ]

    operations = [
        migrations.AlterModelTable(
            name='articleauthor',
            table='articleAuthor',
        ),
        migrations.AlterModelTable(
            name='articlecategory',
            table='articleCategory',
        ),
        migrations.AlterModelTable(
            name='articleimages',
            table='articleImages',
        ),
        migrations.AlterModelTable(
            name='articletags',
            table='articleTags',
        ),
        migrations.AlterModelTable(
            name='articletopics',
            table='articleTopics',
        ),
        migrations.AlterModelTable(
            name='articlevideo',
            table='articleVideo',
        ),
        migrations.AlterModelTable(
            name='articleview',
            table='articleView',
        ),
    ]
