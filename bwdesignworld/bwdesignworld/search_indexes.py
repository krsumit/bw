import datetime
from haystack import indexes
from django.http import HttpResponse, HttpResponseRedirect, HttpResponsePermanentRedirect
from haystack.query import SearchQuerySet
from django.db.models import Q
from django.shortcuts import render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.conf import settings
import json, requests

from articles.models import Articles
from author.models import Author
from sponsored.models import Sponsoredposts

from bwdesignworld.utils import sidebar_data, category_jump_list

# Article search
def search_articles(request):
    if(request.GET.get('q')):
        q = request.GET.get('q')
    else:
        q = ''

    page = request.GET.get('page')

    if (' ' in q) == True:
        count_dta = {
            "query": {
                "match_phrase": { "article_title": q }
            }
        }
    else:
        count_dta = {
            "query": {
                "query_string": { "query": q }
            }
        }
    total_results = requests.get(settings.AWS_ELASTICSEARCH_URL + settings.AWS_ELASTICSEARCH_INDEX + 'articles/_count', data=json.dumps(count_dta))
    tlt_count = total_results.json()

    no_of_pages = range(1, tlt_count['count'], 10)
    #return HttpResponse(tlt_count['count'] / 10)
    if(tlt_count['count'] % 10 == 0):
        last_page = tlt_count['count'] / 10
    else:
        last_page = (tlt_count['count'] / 10) + 1
    pg_url = page

    if(page):
        page_no = int(page)
        from_elem = (page_no-1)*10
        if (' ' in q) == True:
            data = {
                "sort": {
                    "article_published_date": { "order": "desc" }
                },
                "query": {
                    "match_phrase": { "article_title": q }
                },
                "from": from_elem,
                "size":10
            }
        else:
            data = {
                "sort": {
                    "article_published_date": { "order": "desc" }
                },
                "query": {
                    "query_string": { "query": q }
                },
                "from": from_elem,
                "size":10
            }
    else:
        # If page is not an integer, deliver first page.
        if (' ' in q) == True:
            data = {
                "sort": {
                    "article_published_date": { "order": "desc" }
                },
                "query": {
                    "match_phrase": { "article_title": q }
                },
                "from": 0,
                "size":10,

            }
        else:
            data = {
                "sort": {
                    "article_published_date": { "order": "desc" }
                },
                "query": {
                    "query_string": { "query": q }
                },
                "from": 0,
                "size":10,

            }
        pg_url = 1
        page_no = 1

    #return HttpResponse(json.dumps(data))
    result_response = requests.get(settings.AWS_ELASTICSEARCH_URL + settings.AWS_ELASTICSEARCH_INDEX + 'articles/_search', data=json.dumps(data))

    response_dta = result_response.json()
    #return HttpResponse(json.dumps(response_dta['hits']['hits']))

    adjacent_pages = 5
    if(page_no < adjacent_pages):
        start_page = 1
    else:
        if(page_no <= (last_page - 5)):
            start_page = page_no
        else:
            start_page = last_page - 4

    end_page = page_no + adjacent_pages
    if(end_page > last_page):
        end_page = last_page + 1

    page_numbers = [n for n in \
                    range(start_page, end_page)]

    #Sidebar and other data to be used in base template
    sidebar_dta = sidebar_data()
    category_jumlist = category_jump_list()

    meta_title = 'Search Result: '+q+' - BWdefence'
    meta_description = 'Articles, Photos, News and Opinion about '+q
    meta_keyword = q+',  BWdefence'

    og_title= 'Search Result: '+q+' - BWdefence'
    og_url= '/search/articles?q='+q+'&page='+str(pg_url)
    og_image= settings.AWS_S3_BASE_URL + settings.BUCKET_PATH +'static_bwdefence/images/BWH-Logo-300x72.jpg'



    return render(request, 'search/search_article.html', {
        'query': q,
        'articles': response_dta,
        'sidebar_recent_articles': sidebar_dta['sidebar_recent_articles'],
        'trending_now_topics': sidebar_dta['trending_now_topics'],
        'bwtv_articles': sidebar_dta['bwtv_articles'],
        'videomaster_listing': sidebar_dta['videomaster_listing'],
        'category_jumlist': category_jumlist,
        'meta_title': meta_title,
        'meta_description': meta_description,
        'meta_keyword': meta_keyword,
        'og_title': og_title,
        'og_url': og_url,
        'og_image': og_image,
        'page_numbers': page_numbers,
        'show_first': 1 not in page_numbers,
        'show_last': last_page not in page_numbers,
        'last_page': last_page,
        'current_page': page_no,
        'previous_page': int(page_no) - 1,
        'next_page': int(page_no) + 1
    })

# Author search
def search_author(request):
    if(request.GET.get('q')):
        q = request.GET.get('q')
    else:
        q = ''
    page = request.GET.get('page')

    count_dta = {
        "query": {
            "query_string": { "query": q }
        }
    }
    total_results = requests.get(settings.AWS_ELASTICSEARCH_URL + settings.AWS_ELASTICSEARCH_INDEX + 'author/_count', data=json.dumps(count_dta))
    tlt_count = total_results.json()

    no_of_pages = range(1, tlt_count['count'], 10)
    #return HttpResponse(tlt_count['count'] / 10)
    if(tlt_count['count'] % 10 == 0):
        last_page = tlt_count['count'] / 10
    else:
        last_page = (tlt_count['count'] / 10) + 1
    pg_url = page

    if(page):
        page_no = int(page)
        from_elem = (page_no-1)*10
        data = {
            "sort": {
                "author_name": { "order": "desc" }
            },
            "query": {
                "query_string": { "query": q }
            },
            "from": from_elem,
            "size":10
        }

    else:
        # If page is not an integer, deliver first page.
        data = {
            "sort": {
                "author_name": { "order": "desc" }
            },
            "query": {
                "query_string": { "query": q }
            },
            "from": 0,
            "size":10,

        }
        pg_url = 1
        page_no = 1

    result_response = requests.get(settings.AWS_ELASTICSEARCH_URL + settings.AWS_ELASTICSEARCH_INDEX + 'author/_search', data=json.dumps(data))

    response_dta = result_response.json()
    #return HttpResponse(json.dumps(response_dta['hits']['hits']['_source']))

    adjacent_pages = 5
    if(page_no < adjacent_pages):
        start_page = 1
    else:
        if(page_no <= (last_page - 5)):
            start_page = page_no
        else:
            start_page = last_page - 4

    end_page = page_no + adjacent_pages
    if(end_page > last_page):
        end_page = last_page + 1

    page_numbers = [n for n in \
                    range(start_page, end_page)]

    #Sidebar and other data to be used in base template
    sidebar_dta = sidebar_data()
    category_jumlist = category_jump_list()

    meta_title = 'Search Result: '+q+' - BWdefence'
    meta_description = 'BW writer and columnist - '+q+'. Articles written by '+q
    meta_keyword = q+', BWdefence'

    og_title= 'Search Result: '+q+' - BWdefence'
    og_url= '/search/authors?q='+q+'&page='+str(pg_url)
    og_image= settings.AWS_S3_BASE_URL + settings.BUCKET_PATH +'static_bwdiff/images/BWH-Logo-300x72.jpg'

    return render(request, 'search/search_author.html', {
        'query': q,
        'authors': response_dta,
        'sidebar_recent_articles': sidebar_dta['sidebar_recent_articles'],
        'trending_now_topics': sidebar_dta['trending_now_topics'],
        'bwtv_articles': sidebar_dta['bwtv_articles'],
        'videomaster_listing': sidebar_dta['videomaster_listing'],
        'category_jumlist': category_jumlist,
        'meta_title': meta_title,
        'meta_description': meta_description,
        'meta_keyword': meta_keyword,
        'og_title': og_title,
        'og_url': og_url,
        'og_image': og_image,
        'page_numbers': page_numbers,
        'show_first': 1 not in page_numbers,
        'show_last': last_page not in page_numbers,
        'last_page': last_page,
        'current_page': page_no,
        'previous_page': int(page_no) - 1,
        'next_page': int(page_no) + 1
    })

# Sponsored search
def search_sponsored(request):
    q = request.GET.get('q')
    articles_search = SearchQuerySet().models(Sponsoredposts).filter(Q(sponsoredposts_title__contains=q) | Q(sponsoredposts_desc__contains=q) | Q(sponsoredposts_sum__contains=q)).order_by('-pub_date')
    paginator = Paginator(articles_search, 6) # Show 6 articles per page

    page = request.GET.get('page')
    no_of_pages = range(1, paginator.num_pages+1)
    pg_url = page

    try:
        articles = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        articles = paginator.page(1)
        pg_url = 1

    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        articles = paginator.page(paginator.num_pages)

    #Sidebar and other data to be used in base template
    sidebar_dta = sidebar_data()
    category_jumlist = category_jump_list()

    meta_title = 'Search Result: '+q+' - BWdefence'
    meta_description = 'Sponsored Articles, Photos, News and Opinion about '+q
    meta_keyword = q+', BWdefence'

    og_title= 'Search Result: '+q+' - BWdefence'
    og_url= '/search/articles?q='+q+'&page='+str(pg_url)
    og_image= settings.AWS_S3_BASE_URL + settings.BUCKET_PATH +'static_bwdiff/images/BWH-Logo-300x72.jpg'

    return render(request, 'search/search_sponsored.html', {
        'query': q,
        'articles': articles,
        'sidebar_recent_articles': sidebar_dta['sidebar_recent_articles'],
        'trending_now_topics': sidebar_dta['trending_now_topics'],
        'bwtv_articles': sidebar_dta['bwtv_articles'],
        'videomaster_listing': sidebar_dta['videomaster_listing'],
        'category_jumlist': category_jumlist,
        'meta_title': meta_title,
        'meta_description': meta_description,
        'meta_keyword': meta_keyword,
        'og_title': og_title,
        'og_url': og_url,
        'og_image': og_image,
    })
