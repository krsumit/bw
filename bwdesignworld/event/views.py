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
from bwdesignworld.utils import sidebar_data, category_jump_list, closeDbConnection
from event.models import Event
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
def event_listing(request):

    meta_title = 'Events - BW defence'
    meta_description = 'News and Updates for defence in India and World - BW defence'
    meta_keyword = 'News and Updates for defence in India'
    return render(request, 'event/events_listing.html', {
        'meta_title': meta_title,
        'meta_description': meta_description,
        'meta_keyword': meta_keyword,
       
    })

def past_event_articles(request):
    sidebar_zedo_ad = ''

    sidebar_dta = sidebar_data()
    category_jumlist = category_jump_list()
    event_articles = Event.objects.raw("SELECT *, datediff(end_date,CURDATE()) as datedi FROM event  where  end_date <=  CURDATE() AND  valid = 1 ORDER BY  datedi  desc")

    paginator = Paginator(list(event_articles), 2) # Show 10 articles per page

    page = request.GET.get('page')
    no_of_pages = range(1, paginator.num_pages+1)

    try:
        event_articles = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        event_articles = paginator.page(1)

    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        event_articles = paginator.page(paginator.num_pages)

    return render(request, 'event/past_event_listing.html', {
        'event_articles': event_articles,
        #'arcticleall_event':arcticleall_event,
        'no_of_pages': no_of_pages,
        'category_jumlist': category_jumlist,
        'quick_bytes_listing': sidebar_dta['quick_bytes_listing'],
        'sidebar_recent_articles': sidebar_dta['sidebar_recent_articles'],
        'trending_now_topics': sidebar_dta['trending_now_topics'],
        'sidebar_zedo_ad': sidebar_zedo_ad,
    })
