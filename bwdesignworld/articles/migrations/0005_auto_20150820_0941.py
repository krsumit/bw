# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0004_auto_20150820_0935'),
    ]

    operations = [
        migrations.AlterField(
            model_name='articleimages',
            name='article_id',
            field=models.ForeignKey(related_name='image_for_article', blank=b'true', to='articles.Articles', null=b'true'),
        ),
    ]
