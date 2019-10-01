# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tags', '0002_auto_20150820_0848'),
        ('category', '0002_auto_20150820_0848'),
        ('topics', '0002_auto_20150820_0848'),
        ('articles', '0003_auto_20150820_0913'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='articlecategory',
            name='article_id',
        ),
        migrations.AddField(
            model_name='articlecategory',
            name='article_id',
            field=models.ForeignKey(blank=b'true', to='articles.Articles', null=b'true'),
        ),
        migrations.RemoveField(
            model_name='articlecategory',
            name='category',
        ),
        migrations.AddField(
            model_name='articlecategory',
            name='category',
            field=models.ForeignKey(blank=b'true', to='category.ChannelCategory', null=b'true'),
        ),
        migrations.RemoveField(
            model_name='articletags',
            name='article_id',
        ),
        migrations.AddField(
            model_name='articletags',
            name='article_id',
            field=models.ForeignKey(blank=b'true', to='articles.Articles', null=b'true'),
        ),
        migrations.RemoveField(
            model_name='articletags',
            name='tag_id',
        ),
        migrations.AddField(
            model_name='articletags',
            name='tag_id',
            field=models.ForeignKey(blank=b'true', to='tags.ChannelTags', null=b'true'),
        ),
        migrations.RemoveField(
            model_name='articletopics',
            name='article_id',
        ),
        migrations.AddField(
            model_name='articletopics',
            name='article_id',
            field=models.ForeignKey(blank=b'true', to='articles.Articles', null=b'true'),
        ),
        migrations.RemoveField(
            model_name='articletopics',
            name='topic_id',
        ),
        migrations.AddField(
            model_name='articletopics',
            name='topic_id',
            field=models.ForeignKey(blank=b'true', to='topics.ChannelTopics', null=b'true'),
        ),
    ]
