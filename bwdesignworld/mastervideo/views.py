# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.http import HttpResponse
import datetime
from django.http import Http404
from django.template import RequestContext, loader
import pprint
import string
from django.conf import settings
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from bwdesignworld.utils import sidebar_data, category_jump_list, closeDbConnection
# Create your views here.
from mainvideo.models import VideoMain



def main_video_listing(request):
    videomain_listing = VideoMain.objects.raw("SELECT *  FROM video_main  ORDER BY  video_id DESC ")
    meta_title = 'Latest video-feature, Analysis, Opinion - bwhr'
    meta_description = 'Latest video-feature, Opinion, Analysis in bw people'
    meta_keyword = 'Recent Video-feature, people'

    og_title= 'bwpeople | Recent Video-feature'
    og_url= '/all-video-features'
    og_image= settings.AWS_S3_BASE_URL + settings.BUCKET_PATH +'static_bwhr/images/BW-people-logo.jpg'

    paginator = Paginator(list(videomain_listing), 25) # Show 6 articles per page

    page = request.GET.get('page')
    no_of_pages = range(1, paginator.num_pages+1)
    pg_url = page

    try:
        videomain_listing = paginator.page(page)
        page_no = int(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        videomain_listing = paginator.page(1)
        pg_url = 1
        page_no = 1

    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        page_no = 1
        videomain_listing = paginator.page(paginator.num_pages)


    adjacent_pages = 5

    #page_numbers = [n for n in \ range(paginator.num_pages - adjacent_pages, paginator.num_pages + adjacent_pages + 1) \ if n > 0 and n <= paginator.num_pages]
    page_numbers = [n for n in \
                    range(page_no - adjacent_pages, page_no + adjacent_pages + 1) \
                    if n > 0 and n <= page_no]
   

    return render(request, 'mainvideo/main_video_listing.html', {
        'videomain_listing':videomain_listing,
        'page_numbers':page_numbers,
        'show_first': 1 not in page_numbers,
        'show_last': paginator.num_pages not in page_numbers,
        'last_page': paginator.num_pages,
        'meta_title':meta_title,
        'meta_description':meta_description,
        'meta_keyword':meta_keyword,
        'og_title':og_title,
        'og_url':og_url,
        'og_image':og_image

    })
def main_video_landing_page(request,video_title,updated_at,video_id):
    sidebar_zedo_ad = ''
    sidebar_dta = sidebar_data()
    category_jumlist = category_jump_list()
    VideoMain_data = VideoMain.objects.filter(video_id=video_id).first()
    videomain_listing = VideoMain.objects.raw("SELECT *  FROM video_main  ORDER BY  video_id DESC LIMIT 0,5 ")
   
    
    #Meta title and descriptons
    meta_title = video_title+'- bwhr'
    og_title= video_title
    if VideoMain_data:
        meta_description = VideoMain_data.video_summary
        og_url= VideoMain_data.get_absolute_url

    if VideoMain_data:
        og_image= settings.AWS_S3_BASE_URL + settings.VIDEO_THUMB +VideoMain_data.video_thumb_name
    else:
        og_image= settings.AWS_S3_BASE_URL + settings.BUCKET_PATH +'static_bwdiff/images/BW-defence-logo.jpg'   


    return render(request, 'mainvideo/main_video_landing_page.html', {
        'VideoMain_data':VideoMain_data,
        'videomain_listing':videomain_listing,
        'category_jumlist': category_jumlist,
        'sidebar_recent_articles': sidebar_dta['sidebar_recent_articles'],
        'trending_now_topics': sidebar_dta['trending_now_topics'],
        'quick_bytes_listing': sidebar_dta['quick_bytes_listing'],
        'bwtv_cat_details': sidebar_dta['bwtv_cat_details'],
        'sidebar_zedo_ad': sidebar_zedo_ad,
        'meta_title':meta_title,
        'meta_description':meta_description,
        'og_url':og_url,
        'og_image':og_image,
        

    })
