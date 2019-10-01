# -*- coding: utf-8 -*-
from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
import datetime
from django.http import Http404
from django.template import RequestContext, loader
import pprint
import re
import string
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.conf import settings

from articles.models import Articles, ArticleImages,ArticleCategory, ArticleTopics
from columns.models import Columns
from author.models import Author, AuthorType

from bwdesignworld.utils import sidebar_data, category_jump_list, closeDbConnection

def column_articles_list(request, column_name, column_id):

    column_details = Columns.objects.raw("SELECT C.*, AU.*, AAU.*, A.* FROM columns C LEFT JOIN author AU ON AU.column_id=C.column_id LEFT JOIN article_author AAU ON AAU.author_id=AU.author_id LEFT JOIN articles A ON A.article_id = AAU.article_id where  AU.author_type = 4 AND  C.column_id = "+column_id )

    #column_author_image = Columns.objects.raw("SELECT C.*,AU.* FROM columns C LEFT JOIN author AU ON AU.column_id=C.column_id  where  AU.author_type = 4 AND  C.column_id = "+column_id+" LIMIT 3 ")
    column_author_image = Author.objects.raw("SELECT C.*, AU.* FROM columns C LEFT JOIN author AU ON AU.column_id=C.column_id  where  AU.author_type = 4 AND  C.column_id = "+column_id+" LIMIT 3 ")

    columnist = Author.objects.raw("SELECT * FROM (SELECT AU.*, AR.article_published_date FROM author AU INNER JOIN article_author ARU ON AU.author_id = ARU.author_id INNER JOIN articles AR ON ARU.article_id = AR.article_id WHERE AU.author_type='4' ORDER BY AR.article_published_date DESC) AS tem GROUP BY tem.author_id LIMIT 6")

    columinist_names = ''
    for c in columnist:
        columinist_names += c.author_name+', '

    columnist_label = AuthorType.objects.filter(author_type_id = '4').first()
    author_label = columnist_label.author_type_for_url

    sidebar_dta = sidebar_data()
    category_jumlist = category_jump_list()

    meta_title = column_details[0].column_name+' - '+columinist_names+' - BW defence'
    meta_description = 'Column Name by '+columinist_names
    meta_keyword = column_details[0].column_name+', '+columinist_names+'  BW defence'

    og_title= 'BW defence | '+column_details[0].column_name
    og_url= '/column/'+column_name+'-'+column_id
    og_image= settings.AWS_S3_BASE_URL + settings.BUCKET_PATH +'static_bwdiff/images/BW-defence-logo.jpg'

    sidebar_zedo_ad = ''

    closeDbConnection()

    return render(request, 'column/column_landing.html',{
        'column_details': column_details,
        'column_author_image': column_author_image,
        'sidebar_recent_articles': sidebar_dta['sidebar_recent_articles'],
        'trending_now_topics': sidebar_dta['trending_now_topics'],
        'quick_bytes_listing': sidebar_dta['quick_bytes_listing'],
        'bwtv_cat_details': sidebar_dta['bwtv_cat_details'],
        'category_jumlist': category_jumlist,
        'columnist': columnist,
        'author_label': author_label,
        'meta_title': meta_title,
        'meta_description': meta_description,
        'meta_keyword': meta_keyword,
        'og_title': og_title,
        'og_url': og_url,
        'og_image': og_image,
        'sidebar_zedo_ad': sidebar_zedo_ad,
    })
