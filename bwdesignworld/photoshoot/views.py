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
from photoshoot.models import PhotoShoot, PhotoShootPhotos, PhotoShootTags


def photo_shoot(request):
    photoshoot_listing = PhotoShoot.objects.raw("SELECT count(*) as counts, ps.*,psp.photo_shoot_photo_url, psp.photo_shoot_image_id , psp.photo_shoot_photo_name FROM photo_shoot_photos psp join photo_shoot ps on  psp.photo_shoot_id=ps.photo_shoot_id group by psp.photo_shoot_id ORDER BY  ps.photo_shoot_id DESC  LIMIT 0,5")
   
    closeDbConnection()

    return render(request, 'photoshoot/photo_shoot.html', {
        'photoshoot_listing':photoshoot_listing

    })
def photo_shoot_listing(request):
    photoshoot_listing = PhotoShoot.objects.raw("SELECT count(*) as counts, ps.*,psp.photo_shoot_photo_url, psp.photo_shoot_image_id , psp.photo_shoot_photo_name FROM photo_shoot_photos psp join photo_shoot ps on  psp.photo_shoot_id=ps.photo_shoot_id group by psp.photo_shoot_id ORDER BY  ps.photo_shoot_id DESC ")
    meta_title = 'Latest photo-feature, Analysis, Opinion - bw People'
    meta_description = 'Latest photo-feature, Opinion, Analysis in bw People'
    meta_keyword = 'Recent Photo-feature, bw People'

    og_title= 'bwpeople | Recent Photo-feature'
    og_url= '/all-photo-features'
    og_image= settings.AWS_S3_BASE_URL + settings.BUCKET_PATH +'static_bwhr/images/BW-people-logo.jpg'

    paginator = Paginator(list(photoshoot_listing), 10) # Show 6 articles per page

    page = request.GET.get('page')
    no_of_pages = range(1, paginator.num_pages+1)
    pg_url = page

    try:
        photoshoot_listing = paginator.page(page)
        page_no = int(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        photoshoot_listing = paginator.page(1)
        pg_url = 1
        page_no = 1

    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        page_no = 1
        photoshoot_listing = paginator.page(paginator.num_pages)


    adjacent_pages = 5

    #page_numbers = [n for n in \ range(paginator.num_pages - adjacent_pages, paginator.num_pages + adjacent_pages + 1) \ if n > 0 and n <= paginator.num_pages]
    page_numbers = [n for n in \
                    range(page_no - adjacent_pages, page_no + adjacent_pages + 1) \
                    if n > 0 and n <= page_no]
   

    return render(request, 'photoshoot/photo_shoot_listing.html', {
        'photoshoot_listing':photoshoot_listing,
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
def photo_shoot_landing_page(request,photo_shoot_title,photo_shoot_updated_at,photo_shoot_id):
    sidebar_zedo_ad = ''
    sidebar_dta = sidebar_data()
    category_jumlist = category_jump_list()
    photoshoot_data = PhotoShoot.objects.raw("SELECT * from  photo_shoot where photo_shoot_id ='"+photo_shoot_id+"' ")
    photoshoot_image = PhotoShoot.objects.raw("SELECT * from  photo_shoot_photos where photo_shoot_id ='"+photo_shoot_id+"' ")
    photoshoot_listing = PhotoShoot.objects.raw("SELECT count(*) as counts, ps.*,psp.photo_shoot_photo_url, psp.photo_shoot_image_id , psp.photo_shoot_photo_name FROM photo_shoot_photos psp join photo_shoot ps on  psp.photo_shoot_id=ps.photo_shoot_id group by psp.photo_shoot_id ORDER BY  ps.photo_shoot_id DESC  LIMIT 0,10")
    
    #Meta title and descriptons
    meta_title = photo_shoot_title+'- bw People'
    og_title= photo_shoot_title
    if len(list(photoshoot_data)) > 0:
        meta_description = photoshoot_data[0].photo_shoot_description   
        og_url= photoshoot_data[0].get_absolute_url

    if len(list(photoshoot_image)) > 0:
        og_image= settings.AWS_S3_BASE_URL + settings.PHOTOSHOOT_IMAGE_PATH +photoshoot_image[0].photo_shoot_photo_name
    else:
        og_image= settings.AWS_S3_BASE_URL + settings.BUCKET_PATH +'static_bwdiff/images/BW-defence-logo.jpg'

    return render(request, 'photoshoot/photo_shoot_landing_page.html', {
        'photoshoot_data':photoshoot_data,
        'photoshoot_image':photoshoot_image,
        'photoshoot_listing':photoshoot_listing,
        'category_jumlist': category_jumlist,
        'quick_bytes_listing': sidebar_dta['quick_bytes_listing'],
        'bwtv_cat_details': sidebar_dta['bwtv_cat_details'],
        'sidebar_recent_articles': sidebar_dta['sidebar_recent_articles'],
        'trending_now_topics': sidebar_dta['trending_now_topics'],
        'sidebar_zedo_ad': sidebar_zedo_ad,
        'meta_title':meta_title,
        'meta_description':meta_description,
        'og_url':og_url,
        'og_image':og_image,
        

    })
