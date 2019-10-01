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

def topic_articles_list(request, topic_name, topic_id):

    top_name = topic_name.replace('-', ' ')

    recent_articles = Articles.objects.raw("SELECT A.*, AU.*, AI.image_url,AI.photopath FROM articles A LEFT JOIN article_author A_A ON A.article_id = A_A.article_id LEFT JOIN author AU ON A_A.author_id = AU.author_id LEFT JOIN article_images AI ON AI.article_id = A.article_id LEFT JOIN article_topics AT ON A.article_id = AT.article_id WHERE AT.topic_id = '"+topic_id+"' AND (AI.image_status='enabled' OR AI.image_status is null) GROUP BY A.article_id ORDER BY A.article_published_date DESC")

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

    meta_title = top_name+' - BW people - News about Indian Hotel Industry and Hospitality Business in India'
    meta_description = 'Follow the latest news about ' +top_name+' in Indian Hospitality Sector'
    meta_keyword = top_name+',  BW people'

    og_title= 'BW pleople | '+top_name
    og_url= '/topics/'+topic_name+'-'+topic_id
    og_image= settings.AWS_S3_BASE_URL + settings.BUCKET_PATH +'static_bwhr/images/BW-people-logo.jpg'

    sidebar_zedo_ad = ''

    closeDbConnection()

    return render(request, 'article/listing.html', {
        "recent_articles": articles,
        'sidebar_recent_articles': sidebar_dta['sidebar_recent_articles'],
        'trending_now_topics': sidebar_dta['trending_now_topics'],
        'bwtv_articles': sidebar_dta['bwtv_articles'],
        'bwtv_cat_details': sidebar_dta['bwtv_cat_details'],
        'no_of_pages': no_of_pages,
        'page_title_h1': 'Latest Articles in '+top_name,
        'listing_page_url': '/topics-list/'+topic_id,
        'view_page_url': '/topics/'+topic_name+'-'+topic_id,
        'category_jumlist': category_jumlist,
        'meta_title': meta_title,
        'meta_description': meta_description,
        'meta_keyword': meta_keyword,
        'og_title': og_title,
        'og_url': og_url,
        'og_image': og_image,
        'sidebar_zedo_ad': sidebar_zedo_ad,
    })

def topic_articles_list_load(request, topic_id):

    recent_articles = Articles.objects.raw("SELECT A.*, AU.*, AI.image_url,AI.photopath FROM articles A LEFT JOIN article_author A_A ON A.article_id = A_A.article_id LEFT JOIN author AU ON A_A.author_id = AU.author_id LEFT JOIN article_images AI ON AI.article_id = A.article_id LEFT JOIN article_topics AT ON A.article_id = AT.article_id WHERE AT.topic_id = '"+topic_id+"' AND (AI.image_status='enabled' OR AI.image_status is null) GROUP BY A.article_id ORDER BY A.article_published_date DESC")

    paginator = Paginator(list(recent_articles), 6) # Show 6 articles per page

    page = request.GET.get('page')
    no_of_pages = range(1, paginator.num_pages+1)

    topic_details = ChannelTopics.objects.filter(topic_id=topic_id).first()
    topic_name = topic_details.topic_name.replace(' ', '-')

    try:
        articles = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        articles = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        articles = paginator.page(paginator.num_pages)

    sidebar_dta = sidebar_data()

    meta_title = topic_details.topic_name+' - BW people - News about Indian Hotel Industry and Hospitality Business in India'
    meta_description = 'Follow the latest news about ' +topic_details.topic_name+' in Indian Hospitality Sector'
    meta_keyword = topic_details.topic_name+',  BW people'

    og_title= 'BW people | '+topic_details.topic_name
    og_url= '/topics/'+topic_name+'-'+topic_id
    og_image= settings.AWS_S3_BASE_URL + settings.BUCKET_PATH +'static_bwhr/images/BW-people-logo.jpg'

    sidebar_zedo_ad = ''

    closeDbConnection()

    return render(request, 'article/listing_load.html', {
        "recent_articles": articles,
        'sidebar_recent_articles': sidebar_dta['sidebar_recent_articles'],
        'trending_now_topics': sidebar_dta['trending_now_topics'],
        'bwtv_articles': sidebar_dta['bwtv_articles'],
        'bwtv_cat_details': sidebar_dta['bwtv_cat_details'],
        'no_of_pages': no_of_pages,
        'meta_title': meta_title,
        'meta_description': meta_description,
        'meta_keyword': meta_keyword,
        'og_title': og_title,
        'og_url': og_url,
        'og_image': og_image,
        'sidebar_zedo_ad': sidebar_zedo_ad,
    })
