from django.core.management.base import BaseCommand, CommandError
from django.core import serializers
from django.template.defaultfilters import date
from django.conf import settings
import json, requests
import re

from articles.models import Articles, ArticleImages
from author.models import Author, AuthorType
from sponsored.models import Sponsoredposts
from libs.models import SearchIndexingTbl

class Command(BaseCommand):
    def handle(self, *args, **options):
        #When re-indexing articles
        '''data = ''
        for p in Articles.objects.all()[10000:12000]:
            title_for_url = re.sub('[^A-Za-z0-9]+', '-', p.article_title)
            article_url = '/article/'+str(title_for_url)+'/'+str(date(p.article_published_date, "d-m-Y"))+'-'+str(p.article_id)
            article_pic = ArticleImages.objects.filter(article_id=p.article_id).filter(image_status='enabled').first()
            if article_pic:
                if p.is_old == 1:
                    article_image = article_pic.image_url
                else:
                    article_image = settings.AWS_S3_BASE_URL + settings.BUCKET_PATH + settings.ARTICLE_IMAGE_LARGE_PATH + article_pic.photopath
            else:
                article_image = ''

            article_published_date = p.article_published_date.replace(tzinfo=None)
            data += '{"index": {"_id": "%s"}}\n' % p.article_id
            data += json.dumps({
                "article_id": p.article_id,
                "article_title": p.article_title,
                "article_summary": p.article_summary,
                "article_description": p.article_description,
                "article_published_date": str(article_published_date),
                "article_url": article_url,
                "article_image": article_image
            })+'\n'
            #print(data)
        response = requests.post(settings.AWS_ELASTICSEARCH_URL + settings.AWS_ELASTICSEARCH_INDEX + 'articles/_bulk', data=data)
        print response.text'''
        #End

        #Articles
        last_indexed_article = SearchIndexingTbl.objects.filter(tbl_name='article').first()
        #print(last_indexed_article.last_inserted_index_id)
        if(last_indexed_article.last_inserted_index_id == 0):
            articles_list = Articles.objects.all()
        else:
            articles_list = Articles.objects.filter(article_id__gt=last_indexed_article.last_inserted_index_id).order_by('article_id')
        #print(articles_list.article_id)
        if(articles_list):
            data = ''
            for p in articles_list:
                title_for_url = re.sub('[^A-Za-z0-9]+', '-', p.article_title)
                article_url = '/article/'+str(title_for_url)+'/'+str(date(p.article_published_date, "d-m-Y"))+'-'+str(p.article_id)
                article_pic = ArticleImages.objects.filter(article_id=p.article_id).filter(image_status='enabled').first()
                if article_pic:
                    if p.is_old == 1:
                        article_image = article_pic.image_url
                    else:
                        article_image = settings.AWS_S3_BASE_URL + settings.BUCKET_PATH + settings.ARTICLE_IMAGE_LARGE_PATH + article_pic.photopath
                else:
                    article_image = ''

                article_published_date = p.article_published_date.replace(tzinfo=None)
                data += '{"index": {"_id": "%s"}}\n' % p.article_id
                data += json.dumps({
                    "article_id": p.article_id,
                    "article_title": p.article_title,
                    "article_summary": p.article_summary,
                    "article_description": p.article_description,
                    "article_published_date": str(article_published_date),
                    "article_url": article_url,
                    "article_image": article_image
                })+'\n'
            #print(data)
            response = requests.put(settings.AWS_ELASTICSEARCH_URL + settings.AWS_ELASTICSEARCH_INDEX + 'articles/_bulk', data=data)

            last_article_id = articles_list.reverse()[0]
            last_indexed_article.last_inserted_index_id = last_article_id.article_id  # change field
            last_indexed_article.save() # this will update only
        #print(last.article_id)

            print response.text

        # Authors

        last_indexed_author = SearchIndexingTbl.objects.filter(tbl_name='author').first()
        if(last_indexed_author.last_inserted_index_id == 0):
            author_list = Author.objects.all()
        else:
            author_list = Author.objects.filter(author_id__gt=last_indexed_author.last_inserted_index_id).order_by('author_id')

        if (author_list):
            data = ''
            for p in author_list:
                author_label_val = AuthorType.objects.filter(author_type_id=p.author_type).first()
                author_label = author_label_val.label.strip().replace(' ', '-')
                author_name_for_url = p.author_name.strip().replace(' ', '-')
                author_url = '/author/'+str(author_label)+'/'+str(author_name_for_url)+'-'+str(p.author_id)
                #author_url = p.get_absolute_url
                if p.author_photo:
                    author_image = settings.AWS_S3_BASE_URL + settings.BUCKET_PATH + settings.AUTHOR_IMAGE_PATH + p.author_photo
                else:
                    author_image = settings.AWS_S3_BASE_URL + settings.BUCKET_PATH + "static_bwhotelier/images/author_dummy.png"

                data += '{"index": {"_id": "%s"}}\n' % p.author_id
                data += json.dumps({
                    "author_name": p.author_name,
                    "author_url": author_url,
                    "author_image": author_image
                })+'\n'
            response = requests.put(settings.AWS_ELASTICSEARCH_URL + settings.AWS_ELASTICSEARCH_INDEX + 'author/_bulk', data=data)

            last_author_id = author_list.reverse()[0]
            last_indexed_author.last_inserted_index_id = last_author_id.author_id  # change field
            last_indexed_author.save() # this will update only

            print response.text


        # Sponsored
        '''data = ''
        for p in Sponsoredposts.objects.all():
            data += '{"index": {"_id": "%s"}}\n' % p.sponsoredposts_id
            data += json.dumps({
                "sponsoredposts_title": p.sponsoredposts_title,
                "sponsoredposts_sum": p.sponsoredposts_description,
                "sponsoredposts_desc": p.sponsoredposts_summary,
                "sponsored_published_date": str(p.sponsoredposts_published_date)
            })+'\n'
        response = requests.put(settings.AWS_ELASTICSEARCH_URL + settings.AWS_ELASTICSEARCH_INDEX + 'sponsored/_bulk', data=data)
        print response.text'''
