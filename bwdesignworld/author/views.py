# -*- coding: utf-8 -*-
from django.shortcuts import render
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
#from featuredbox.models import FeatureBox
from author.models import Author, AuthorType
from topics.models import ChannelTopics
from tags.models import ChannelTags
from columns.models import Columns
from category.models import ChannelCategory

from bwdesignworld.utils import sidebar_data, category_jump_list, closeDbConnection

# Create your views here.

def author_articles_list(request, author_type, author_name, author_id):

    auth_name = author_name.replace('-', ' ')
    auth_type = author_type.replace('-', ' ')

    author_details = Author.objects.raw("SELECT AU.*, AUTYPE.* FROM author AU LEFT JOIN author_type AUTYPE ON AU.author_type = AUTYPE.author_type_id WHERE AU.author_id = '"+author_id+"' AND AUTYPE.label = '"+auth_type+"'")

    column_details = ''
    if author_details[0].author_type == 4:
        column_details = Columns.objects.raw("SELECT C.* FROM columns C LEFT JOIN author AU ON AU.column_id = C.column_id WHERE AU.author_id = "+str(author_details[0].author_id))
    if len(list(column_details)) > 0:
        column_details_data = column_details[0]
    else:
        column_details_data = ''

    recent_articles = Articles.objects.raw("SELECT A.*, AU.*, AI.photopath,AI.image_url FROM articles A LEFT JOIN article_author A_A ON A.article_id = A_A.article_id LEFT JOIN author AU ON A_A.author_id = AU.author_id LEFT JOIN article_images AI ON AI.article_id = A.article_id WHERE AU.author_id = '"+author_id+"' AND (AI.image_status='enabled' OR AI.image_status is null) GROUP BY A.article_id ORDER BY A.article_published_date DESC")

    paginator = Paginator(list(recent_articles), 6) # Show 6 articles per page

    page = request.GET.get('page')
    no_of_pages = range(1, paginator.num_pages+1)

    try:
        articles = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        articles = paginator.page(1)

    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        articles = paginator.page(paginator.num_pages)

    sidebar_dta = sidebar_data()
    category_jumlist = category_jump_list()

    meta_title = auth_name+' - BW defence'
    meta_description = 'Latest news and analysis written by '+auth_name+'.'+ author_details[0].author_bio
    meta_keyword = auth_name+',  BW defence'

    og_title= 'BW defence | '+auth_name
    og_url= '/author/'+author_type+'/'+author_name+'-'+author_id
    og_image = settings.AWS_S3_BASE_URL + settings.BUCKET_PATH +'static_bwdiff/images/BW-defence-logo.jpg'

    columnist = Author.objects.raw("SELECT * FROM (SELECT au.*,ar.article_published_date FROM author au INNER JOIN article_author aru ON au.author_id=aru.author_id INNER JOIN articles ar ON aru.article_id=ar.article_id WHERE au.author_type='4' ORDER BY ar.article_published_date DESC) AS tem GROUP BY tem.author_id LIMIT 9")
    #columnist = Author.objects.filter(author_type='4')[:9]

    sidebar_zedo_ad = ''

    closeDbConnection()

    return render(request, 'article/author_article_listing.html', {
        "recent_articles": articles,
        'sidebar_recent_articles': sidebar_dta['sidebar_recent_articles'],
        'trending_now_topics': sidebar_dta['trending_now_topics'],
        'quick_bytes_listing': sidebar_dta['quick_bytes_listing'],
        'bwtv_cat_details': sidebar_dta['bwtv_cat_details'],
        'no_of_pages': no_of_pages,
        'page_title_h1': 'Latest Articles By '+auth_name,
        'listing_page_url': '/author-load/'+author_type+'/'+author_id,
        'view_page_url': '/author/'+author_type+'/'+author_name+'-'+author_id,
        'author_details': author_details,
        'column_details': column_details_data,
        'columnist': columnist,
        'category_jumlist': category_jumlist,
        'meta_title': meta_title,
        'meta_description': meta_description,
        'meta_keyword': meta_keyword,
        'og_title': og_title,
        'og_url': og_url,
        'og_image': og_image,
        'sidebar_zedo_ad': sidebar_zedo_ad,
    })

def author_articles_list_load(request, author_type, author_id):

    recent_articles = Articles.objects.raw("SELECT A.*, AU.*, AI.image_url FROM articles A LEFT JOIN article_author A_A ON A.article_id = A_A.article_id LEFT JOIN author AU ON A_A.author_id = AU.author_id LEFT JOIN article_images AI ON AI.article_id = A.article_id WHERE AU.author_id = '"+author_id+"' AND AU.author_type = '"+author_type+"'  AND (AI.image_status='enabled' OR AI.image_status is null) GROUP BY A.article_id ORDER BY A.article_published_date DESC")

    paginator = Paginator(list(recent_articles), 6) # Show 6 articles per page

    page = request.GET.get('page')
    no_of_pages = range(1, paginator.num_pages+1)

    try:
        articles = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        articles = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        articles = paginator.page(paginator.num_pages)
    sidebar_dta = sidebar_data()

    sidebar_zedo_ad = ''

    closeDbConnection()

    return render(request, 'article/listing_load.html', {
        "recent_articles": articles,
        'sidebar_recent_articles': sidebar_dta['sidebar_recent_articles'],
        'trending_now_topics': sidebar_dta['trending_now_topics'],
        'quick_bytes_listing': sidebar_dta['quick_bytes_listing'],
        'bwtv_cat_details': sidebar_dta['bwtv_cat_details'],
        'no_of_pages': no_of_pages,
        'sidebar_zedo_ad': sidebar_zedo_ad,
    })

def author_details(request, author_type, author_name, author_id):
    return render(request, 'article/article_landing_with_author.html',{

    })
