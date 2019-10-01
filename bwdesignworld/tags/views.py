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

from articles.models import Articles, ArticleImages,ArticleCategory, ArticleTopics, ArticleTags
#from featuredbox.models import FeatureBox
from author.models import Author, AuthorType
from topics.models import ChannelTopics
from tags.models import ChannelTags
from columns.models import Columns
from category.models import ChannelCategory

from bwdesignworld.utils import sidebar_data, category_jump_list, closeDbConnection

# Create your views here.

def tag_articles_list(request, tag_name, tag_id):

    top_name = tag_name.replace('-', ' ')

    recent_articles = Articles.objects.raw("SELECT A.*, AU.*, AI.image_url,AI.photopath FROM articles A LEFT JOIN article_author A_A ON A.article_id = A_A.article_id LEFT JOIN author AU ON A_A.author_id = AU.author_id LEFT JOIN article_images AI ON AI.article_id = A.article_id LEFT JOIN article_tags AT ON A.article_id = AT.article_id WHERE AT.tag_id = '"+tag_id+"' AND (AI.image_status='enabled' OR AI.image_status is null) GROUP BY A.article_id ORDER BY A.article_published_date DESC")

    paginator = Paginator(list(recent_articles), 10) # Show 6 articles per page

    page = request.GET.get('page')
    no_of_pages = range(1, paginator.num_pages+1)
    pg_url = page

    try:
        recent_articles = paginator.page(page)
        page_no = int(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        recent_articles = paginator.page(1)
        pg_url = 1
        page_no = 1

    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        page_no = 1
        recent_articles = paginator.page(paginator.num_pages)


    adjacent_pages = 5

    #page_numbers = [n for n in \ range(paginator.num_pages - adjacent_pages, paginator.num_pages + adjacent_pages + 1) \ if n > 0 and n <= paginator.num_pages]
    page_numbers = [n for n in \
                    range(page_no - adjacent_pages, page_no + adjacent_pages + 1) \
                    if n > 0 and n <= page_no]

    sidebar_dta = sidebar_data()
    category_jumlist = category_jump_list()

    meta_title = top_name+' - BW people - News about Indian Hotel Industry and Hospitality Business in India'
    meta_description = 'Follow the latest news about ' +top_name+' in Indian Hospitality Sector'
    meta_keyword = top_name+',  BW people'

    og_title= 'BW people | '+top_name
    og_url= '/tags/'+tag_name+'-'+tag_id
    og_image= settings.AWS_S3_BASE_URL + settings.BUCKET_PATH +'static_bwhr/images/BW-people-logo.jpg'

    sidebar_zedo_ad = ''

    closeDbConnection()

    return render(request, 'article/listing.html', {
        "news_articles": recent_articles,
        'sidebar_recent_articles': sidebar_dta['sidebar_recent_articles'],
        'trending_now_topics': sidebar_dta['trending_now_topics'],
        'bwtv_articles': sidebar_dta['bwtv_articles'],
        'bwtv_cat_details': sidebar_dta['bwtv_cat_details'],
        'no_of_pages': no_of_pages,
        'page_title_h1': 'Latest Articles in '+top_name,
        'listing_page_url': '/tags-list/'+tag_id,
        'view_page_url': '/tags/'+tag_name+'-'+tag_id,
        'category_jumlist': category_jumlist,
        'meta_title': meta_title,
        'meta_description': meta_description,
        'meta_keyword': meta_keyword,
        'og_title': og_title,
        'og_url': og_url,
        'og_image': og_image,
        'sidebar_zedo_ad': sidebar_zedo_ad,
        'page_numbers':page_numbers,
        'show_first': 1 not in page_numbers,
        'show_last': paginator.num_pages not in page_numbers,
        'last_page': paginator.num_pages
    })

def tag_articles_list_load(request, tag_id):

    recent_articles = Articles.objects.raw("SELECT A.*, AU.*, AI.image_url,AI.photopath FROM articles A LEFT JOIN article_author A_A ON A.article_id = A_A.article_id LEFT JOIN author AU ON A_A.author_id = AU.author_id LEFT JOIN article_images AI ON AI.article_id = A.article_id LEFT JOIN article_tags AT ON A.article_id = AT.article_id WHERE AT.tag_id = '"+tag_id+"' AND (AI.image_status='enabled' OR AI.image_status is null) GROUP BY A.article_id ORDER BY A.article_published_date DESC")

    paginator = Paginator(list(recent_articles), 6) # Show 6 articles per page

    page = request.GET.get('page')
    no_of_pages = range(1, paginator.num_pages+1)

    tag_details = ChannelTags.objects.filter(tag_id=tag_id).first()
    tag_name = tag_details.tag_name.replace(' ', '-')

    try:
        articles = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        articles = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        articles = paginator.page(paginator.num_pages)

    sidebar_dta = sidebar_data()

    meta_title = tag_details.tag_name+' - BW people - News about Indian Hotel Industry and Hospitality Business in India'
    meta_description = 'Follow the latest news about ' +tag_details.tag_name+' in Indian Hospitality Sector'
    meta_keyword = tag_details.tag_name+',  BW people'

    og_title= 'BW people | '+tag_details.tag_name
    og_url= '/tags/'+tag_name+'-'+tag_id
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


def tag_listing(request, tag_name, tag_id):
    return render(request, 'article/article_landing_with_author.html',{

    })

def tag_redirect(request, tag_name):
    top_name = tag_name.replace('-', ' ')
    tag_details = ChannelTags.objects.filter(tag_name=top_name).first()
    #return HttpResponse(category_details)
    #return HttpResponsePermanentRedirect('/tags/' + tag_name + '-' + str(tag_details.tag_id))
    if not tag_details:
        return HttpResponseRedirect("/")
    else:
        tag_name = re.sub('[^A-Za-z0-9]+', '-', tag_details.tag_name)
        return HttpResponsePermanentRedirect('/tags/' + tag_name + '-' + str(tag_details.tag_id))
