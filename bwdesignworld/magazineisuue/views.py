# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.http import HttpResponse
import datetime
from django.utils import timezone
from django.http import HttpResponseRedirect
from django.http import HttpResponse
import json
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger,InvalidPage
from django.conf import settings
# Create your views here.
from magazineisuue.models import Magazine
from bwdesignworld.utils import sidebar_data, category_jump_list, closeDbConnection

def magazineissue_listing(request, year):
    meta_title = 'BW defence Magazine – '+str(year)+' Issues'
    meta_description = 'BW defence Magazine is one of the most popular and respected News and Updates for defence in India. Here is a list of issues released in '+str(year)
    meta_keyword = 'Web Exclusive, News and Updates for defence in India, News and Updates for defence in India'
    og_title = 'BW defence Magazine – '+str(year)+' Issues'
    og_url = '/magazine -issue'
    og_image = settings.AWS_S3_BASE_URL + settings.BUCKET_PATH +'static_bwhr/images/BW-defence-logo.jpg'
    category_jumlist = category_jump_list()
    magazine_allyear = Magazine.objects.raw("SELECT magazine_id , YEAR(publish_date_m) as years FROM magazine  GROUP BY YEAR(publish_date_m) ORDER BY publish_date_m DESC ")
    if request.method == 'GET':

        if(year!=''):
            magazine_listing = Magazine.objects.raw("SELECT * FROM magazine  WHERE YEAR(publish_date_m) = '"+year+"' ORDER BY publish_date_m DESC ")
        return render(request, 'magazineissue/magazineissue_listing.html', {
            'meta_title': meta_title,
            'meta_description': meta_description,
            'meta_keyword': meta_keyword,
            'og_title':og_title,
            'og_url':og_url,
            'og_image':og_image,
            'magazine_allyear':magazine_allyear,
            'magazine_listing':magazine_listing,
            'category_jumlist':category_jumlist,
            'year':year

        })
