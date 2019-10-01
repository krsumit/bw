# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tags', '0002_auto_20150820_0848'),
        ('category', '0002_auto_20150820_0848'),
        ('topics', '0002_auto_20150820_0848'),
        ('articles', '0002_auto_20150820_0848'),
    ]

    operations = [
        migrations.AddField(
            model_name='articlecategory',
            name='article_id',
            field=models.ManyToManyField(to='articles.Articles', blank=b'true'),
        ),
        migrations.AddField(
            model_name='articlecategory',
            name='category',
            field=models.ManyToManyField(to='category.ChannelCategory', blank=b'true'),
        ),
        migrations.AddField(
            model_name='articleimages',
            name='article_id',
            field=models.ForeignKey(blank=b'true', to='articles.Articles', null=b'true'),
        ),
        migrations.AddField(
            model_name='articles',
            name='display_to_homepage',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='articletags',
            name='article_id',
            field=models.ManyToManyField(to='articles.Articles', blank=b'true'),
        ),
        migrations.AddField(
            model_name='articletags',
            name='tag_id',
            field=models.ManyToManyField(to='tags.ChannelTags', blank=b'true'),
        ),
        migrations.AddField(
            model_name='articletopics',
            name='article_id',
            field=models.ManyToManyField(to='articles.Articles', blank=b'true'),
        ),
        migrations.AddField(
            model_name='articletopics',
            name='topic_id',
            field=models.ManyToManyField(to='topics.ChannelTopics', blank=b'true'),
        ),
        migrations.AddField(
            model_name='articlevideo',
            name='article_id',
            field=models.ForeignKey(blank=b'true', to='articles.Articles', null=b'true'),
        ),
        migrations.AddField(
            model_name='articleview',
            name='article_id',
            field=models.ForeignKey(blank=b'true', to='articles.Articles', null=b'true'),
        ),
        migrations.AlterField(
            model_name='articleimages',
            name='id',
            field=models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True),
        ),
    ]
