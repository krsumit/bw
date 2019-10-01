# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, HttpResponsePermanentRedirect
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

def category_articles_list(request, category_name, category_id):

    cat_name = category_name.replace('-', ' ')

    recent_articles = Articles.objects.raw("SELECT A.*, AU.*, AI.image_url,AI.photopath FROM articles A LEFT JOIN article_author A_A ON A.article_id = A_A.article_id LEFT JOIN author AU ON A_A.author_id = AU.author_id LEFT JOIN article_images AI ON AI.article_id = A.article_id LEFT JOIN article_category AC ON A.article_id = AC.article_id WHERE AC.category_id = '"+category_id+"' AND (AI.image_status='enabled' OR AI.image_status is null) GROUP BY A.article_id ORDER BY A.article_published_date DESC")

    paginator = Paginator(list(recent_articles), 10) # Show 10 articles per page

    page = request.GET.get('page')
    no_of_pages = range(1, paginator.num_pages+1)

    try:
        recent_articles = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        recent_articles = paginator.page(1)

    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        recent_articles = paginator.page(paginator.num_pages)

    sidebar_dta = sidebar_data()
    category_jumlist = category_jump_list()

    meta_title = cat_name+' - BW defence - News about News and Updates for defence in India Business in India'
    meta_description = 'Follow the latest news about ' +cat_name+' in News and Updates for defence in India'
    meta_keyword = cat_name+',  BW defence'

    og_title= 'BW defence | '+cat_name
    og_url= '/category/'+category_name+'-'+category_id
    og_image= settings.AWS_S3_BASE_URL + settings.BUCKET_PATH +'static_bwdiff/images/BW-defence-logo.jpg'

    sidebar_zedo_ad = ''

    closeDbConnection()

    return render(request, 'article/listing.html', {
        "news_articles": recent_articles,
        'sidebar_recent_articles': sidebar_dta['sidebar_recent_articles'],
        'trending_now_topics': sidebar_dta['trending_now_topics'],
        'bwtv_articles': sidebar_dta['bwtv_articles'],
        'bwtv_cat_details': sidebar_dta['bwtv_cat_details'],
        'quick_bytes_listing': sidebar_dta['quick_bytes_listing'],
        'no_of_pages': no_of_pages,
        'page_title_h1': 'Latest Articles in '+cat_name,
        'listing_page_url': '/category-list/'+category_id,
        'view_page_url': '/category/'+category_name+'-'+category_id,
        'category_jumlist': category_jumlist,
        'meta_title': meta_title,
        'meta_description': meta_description,
        'meta_keyword': meta_keyword,
        'og_title': og_title,
        'og_url': og_url,
        'og_image': og_image,
        'sidebar_zedo_ad': sidebar_zedo_ad,
    })

def category_articles_list_load(request, category_id):

    #cat_name = ChannelCategory.objects.filter(category_id=category_id).first()

    recent_articles = Articles.objects.raw("SELECT A.*, AU.*, AI.image_url,AI.photopath FROM articles A LEFT JOIN article_author A_A ON A.article_id = A_A.article_id LEFT JOIN author AU ON A_A.author_id = AU.author_id LEFT JOIN article_images AI ON AI.article_id = A.article_id LEFT JOIN article_category AC ON A.article_id = AC.article_id WHERE AC.category_id = '"+category_id+"' AND (AI.image_status='enabled' OR AI.image_status is null) GROUP BY A.article_id ORDER BY A.article_published_date DESC")

    paginator = Paginator(list(recent_articles), 6) # Show 6 articles per page

    page = request.GET.get('page')
    no_of_pages = range(1, paginator.num_pages+1)

    category_details = ChannelCategory.objects.filter(category_id=category_id).first()

    cat_name = str(category_details.category_name)

    try:
        articles = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        articles = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        articles = paginator.page(paginator.num_pages)

    sidebar_dta = sidebar_data()

    meta_title = cat_name+' - BW defence - News about News and Updates for defence in India'
    meta_description = 'Follow the latest news about ' +cat_name+' in News and Updates for defence in India'
    meta_keyword = cat_name+',  BW defence'

    og_title= 'BW defence | '+cat_name
    og_url= '/category/'+str(category_details.category_name_for_url)+'-'+category_id
    og_image= settings.AWS_S3_BASE_URL + settings.BUCKET_PATH +'static_bwdiff/images/BW-defence-logo.jpg'

    sidebar_zedo_ad = ''

    closeDbConnection()

    return render(request, 'article/listing_load.html', {
        "recent_articles": articles,
        'sidebar_recent_articles': sidebar_dta['sidebar_recent_articles'],
        'trending_now_topics': sidebar_dta['trending_now_topics'],
        'quick_bytes_listing': sidebar_dta['quick_bytes_listing'],
        'bwtv_articles': sidebar_dta['bwtv_articles'],
        'bwtv_cat_details': sidebar_dta['bwtv_cat_details'],
        'no_of_pages': no_of_pages,
        'sidebar_zedo_ad': sidebar_zedo_ad,
    })

def category_redirect(request, category_name):
    cat_name = category_name.replace('-', ' ')
    category_details = ChannelCategory.objects.filter(category_name=cat_name).first()
    #return HttpResponse(category_details)
    #return HttpResponseRedirect('/category/' + category_name + '-' + str(category_details.category_id))
    if not category_details:
        return HttpResponseRedirect("/")
    else:
        category_name = re.sub('[^A-Za-z0-9]+', '-', category_details.category_name)
        #return HttpResponseRedirect(category_details.category_self_url())
        return HttpResponsePermanentRedirect('/category/' + category_name + '-' + str(category_details.category_id))
