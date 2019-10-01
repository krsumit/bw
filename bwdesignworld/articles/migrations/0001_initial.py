# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ArticleAuthor',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('article_id', models.IntegerField()),
                ('author_type', models.IntegerField()),
                ('author_id', models.IntegerField()),
            ],
            options={
                'db_table': 'article_author',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='ArticleCategory',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('category_level', models.IntegerField()),
            ],
            options={
                'db_table': 'article_category',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='ArticleImages',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('image_url', models.CharField(max_length=255)),
                ('image_title', models.CharField(max_length=255)),
                ('image_source_name', models.CharField(max_length=100)),
                ('image_source_url', models.CharField(max_length=255)),
                ('image_status', models.CharField(max_length=8)),
            ],
            options={
                'db_table': 'article_images',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Articles',
            fields=[
                ('article_id', models.AutoField(serialize=False, primary_key=True)),
                ('article_title', models.TextField()),
                ('article_description', models.TextField()),
                ('article_summary', models.TextField()),
                ('article_type', models.CharField(max_length=255)),
                ('article_published_date', models.DateTimeField()),
                ('article_slug', models.TextField()),
                ('article_status', models.CharField(max_length=9)),
                ('important_article', models.IntegerField()),
                ('article_location_country', models.CharField(max_length=255)),
                ('article_location_state', models.CharField(max_length=255)),
            ],
            options={
                'db_table': 'articles',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='ArticleTags',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
            ],
            options={
                'db_table': 'article_tags',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='ArticleTopics',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
            ],
            options={
                'db_table': 'article_topics',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='ArticleVideo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('video_url', models.CharField(max_length=255)),
                ('video_embed_code', models.TextField()),
                ('video_title', models.CharField(max_length=255)),
            ],
            options={
                'db_table': 'article_video',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='ArticleView',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('view_date', models.DateField()),
                ('view_time', models.TimeField()),
                ('article_published_date', models.DateField()),
            ],
            options={
                'db_table': 'article_view',
                'managed': False,
            },
        ),
    ]
