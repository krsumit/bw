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
from django.template.defaultfilters import date
import feedparser
from django.conf import settings
from django.db.models import Q

from quickbytes.models import QuickBytes, QuickBytesPhotos, QuickBytesTags
from author.models import Author, AuthorType
from topics.models import ChannelTopics
from tags.models import ChannelTags
from sponsored.models import Sponsoredposts, SponsoredpostsCategory, SponsoredpostsImages, SponsoredpostsView

from bwdesignworld.utils import sidebar_data, category_jump_list, closeDbConnection

# Create your views here.

def quickbyteslanding(request, quick_byte_title, quick_byte_published_date, quick_byte_id):
    sidebar_dta = sidebar_data()
    category_jumlist = category_jump_list()

    sidebar_zedo_ad = '<!-- Javascript tag  --><!-- begin ZEDO for channel:  Quick Bytes LP , publisher: bwhr , Ad Dimension: Medium Rectangle-300x250-QB-LP - 300 x 250 --><script language="JavaScript">var zflag_nid="3336"; var zflag_cid="3"; var zflag_sid="1"; var zflag_width="300"; var zflag_height="250"; var zflag_sz="20";</script><script language="JavaScript" src="http://xp2.zedo.com/jsc/xp2/fo.js"></script><!-- end ZEDO for channel:  Quick Bytes LP , publisher: bwhr , Ad Dimension: Medium Rectangle-300x250-QB-LP - 300 x 250 -->'

    #quickbytes_detail = QuickBytes.objects.raw("SELECT * FROM quick_bytes  WHERE quick_byte_id = "+quick_byte_id+" ")
    quickbytes_detail = QuickBytes.objects.filter(quick_byte_id = quick_byte_id).first()

    if quickbytes_detail:
        author_details = Author.objects.raw("SELECT AU.*, AUTYPE.* FROM author AU INNER JOIN quick_bytes QB ON QB.quick_byte_author_id = AU.author_id JOIN author_type AUTYPE ON AU.author_type = AUTYPE.author_type_id WHERE QB.quick_byte_id = "+quick_byte_id)
        if len(list(author_details)) > 0:
            author_label = author_details[0].label.replace(' ', '-')
        else:
            author_label = ''

        quickbytes_tags = ChannelTags.objects.raw("SELECT t.* FROM channel_tags t INNER JOIN quick_bytes_tags qt ON t.tag_id = qt.tag_id WHERE qt.quick_byte_id = "+quick_byte_id)
        tag_names = ''
        for tag in quickbytes_tags:
            tag_names = tag_names+', '+tag.tag_name

        '''quickbytes_topics = ChannelTopics.objects.raw("SELECT t.* FROM channel_topics t INNER JOIN quick_bytes_topic qt ON t.topic_id = qt.topic_id WHERE qt.quick_byte_id = "+quick_byte_id)
        topic_names = ''
        for topic in quickbytes_topics:
            topic_names = topic_names+', '+topic.topic_name'''

        #related_articles = QuickBytes.objects.raw("SELECT ar.*, ia.quick_byte_photo_url, ia.quick_byte_photo_name, COUNT(*) AS tagcount FROM (SELECT tag_id AS id FROM quick_bytes_tags WHERE quick_byte_id="+quick_byte_id+") AS t1 JOIN  quick_bytes_tags t2 ON t1.id=t2.tag_id JOIN quick_bytes_photos ia ON t2.quick_byte_id=ia.quick_byte_id JOIN quick_bytes ar ON t2.quick_byte_id=ar.quick_byte_id GROUP BY t2.quick_byte_id HAVING t2.quick_byte_id!="+quick_byte_id+" ORDER BY tagcount DESC")

        next_quick_byte = quickbytes_detail.get_next();
        prev_quick_byte = quickbytes_detail.get_prev();

        quick_bytes_image = QuickBytesPhotos.objects.filter(quick_byte_id = quick_byte_id).order_by('sequence').first()
        if quick_bytes_image:
            all_image_sequence_count = QuickBytesPhotos.objects.filter(quick_byte_id = quick_byte_id).filter(Q(sequence=None) | Q(sequence=0)).count()
            if all_image_sequence_count > 1:
                next_quick_byte_pic = quick_bytes_image.get_next_pic_quick_byte()
                prev_quick_byte_pic = quick_bytes_image.get_prev_pic_quick_byte()
            else:
                next_quick_byte_pic = quick_bytes_image.get_next_pic_sequence()
                prev_quick_byte_pic = quick_bytes_image.get_prev_pic_sequence()
        else:
            next_quick_byte_pic = []
            prev_quick_byte_pic = []

        #meta_title = ''
        if len(list(author_details)) > 0:
            page_author_name = author_details[0].author_name
            if author_details[0].author_type != 1 and author_details[0].author_type != 2:
                meta_title = quickbytes_detail.quick_byte_title+'-'+author_details[0].author_name+' - BW defence'
                meta_description = author_details[0].author_name+' - '+quickbytes_detail.quick_byte_description+', '+tag_names
            else:
                meta_title = quickbytes_detail.quick_byte_title+' - BW defence'
                meta_description = quickbytes_detail.quick_byte_description+', '+tag_names
        else:
            page_author_name = 'BW defence'
            meta_title = quickbytes_detail.quick_byte_title+' - BW defence'
            meta_description = quickbytes_detail.quick_byte_description+', '+tag_names
        meta_keyword = tag_names

        og_title= quickbytes_detail.quick_byte_title
        og_url= '/quickbytes/'+quick_byte_title+'/'+quick_byte_published_date+'-'+quick_byte_id
        if not quick_bytes_image:
            og_image= settings.AWS_S3_BASE_URL + settings.BUCKET_PATH +'static_bwdiff/images/BW-defence-logo.jpg'
        else:
            og_image= settings.AWS_S3_BASE_URL + settings.BUCKET_PATH + settings.QUICKBYTES_IMAGE_EXTRA_LARGE_PATH + quick_bytes_image.quick_byte_photo_name

        #sponsored_detail = Sponsoredposts.objects.raw("SELECT S.*, SI.image_url FROM sponsoredposts S LEFT JOIN sponsoredposts_images SI ON SI.sponsoredposts_id = S.sponsoredposts_id  ORDER BY S.sponsoredposts_published_date DESC LIMIT 2")
        #feeds_cric = feedparser.parse('http://bwcio.com/feed/')
        #feeds_bws = feedparser.parse('http://bwsmartcities.com/feed')
        #feeds_bwh = feedparser.parse('http://bwhotelier.com/feed/')

        closeDbConnection()

        return render(request, 'quickbytes/quickbytes_landing.html',{
            'quickbytes_detail': quickbytes_detail,
            #'quickbytes_related_articles': related_articles,
            'sidebar_recent_articles': sidebar_dta['sidebar_recent_articles'],
            'trending_now_topics': sidebar_dta['trending_now_topics'],
            'quick_bytes_listing': sidebar_dta['quick_bytes_listing'],
            'bwtv_cat_details': sidebar_dta['bwtv_cat_details'],
            'next_quick_byte': next_quick_byte,
            'prev_quick_byte': prev_quick_byte,
            'next_quick_byte_pic': next_quick_byte_pic,
            'prev_quick_byte_pic': prev_quick_byte_pic,
            'quick_bytes_image': quick_bytes_image,
            'author_details': author_details,
            'author_label': author_label,
            'quickbytes_tags': quickbytes_tags,
            'category_jumlist': category_jumlist,
            'meta_title': meta_title,
            'meta_description': meta_description,
            'meta_keyword': meta_keyword,
            'og_title': og_title,
            'og_url': og_url,
            'og_image': og_image,
            #'sponsored_detail':sponsored_detail,
            #'feeds_cric':feeds_cric,
            #'feeds_bws':feeds_bws,
            #'feeds_bwh':feeds_bwh,
            'sidebar_zedo_ad': sidebar_zedo_ad,
            'page_author_name': page_author_name,
        })
    else:
        meta_title = 'Quickbytes - BW people'
        meta_description = 'Quickbytes'
        meta_keyword = 'Quickbytes'

        og_title= 'Quickbytes - BW people'
        #og_url= article_detail[0].get_absolute_url
        og_image= settings.AWS_S3_BASE_URL + settings.BUCKET_PATH +'static_bwhr/images/BW-people-logo.jpg'

        return render(request, 'quickbytes/quickbytes_not_found.html',{
            'qyickbytes_content':sidebar_dta['quick_bytes'],
            'sidebar_recent_articles': sidebar_dta['sidebar_recent_articles'],
            'trending_now_topics': sidebar_dta['trending_now_topics'],
            'videomaster_listing': sidebar_dta['videomaster_listing'],
            'bwtv_cat_details': sidebar_dta['bwtv_cat_details'],
            'category_jumlist': category_jumlist,
            'meta_title': meta_title,
            'meta_description': meta_description,
            'meta_keyword': meta_keyword,
            'og_title': og_title,
            #'og_url': og_url,
            'og_image': og_image,
            'sidebar_zedo_ad': sidebar_zedo_ad,
        })

def quick_bytes_image_load(request, quick_byte_title, quick_byte_id, quick_byte_image_name, quick_byte_image_id):

    sidebar_dta = sidebar_data()

    sidebar_zedo_ad = '<!-- Javascript tag  --><!-- begin ZEDO for channel:  Quick Bytes LP , publisher: people , Ad Dimension: Medium Rectangle-300x250-QB-LP - 300 x 250 --><script language="JavaScript">var zflag_nid="3336"; var zflag_cid="3"; var zflag_sid="1"; var zflag_width="300"; var zflag_height="250"; var zflag_sz="20";</script><script language="JavaScript" src="http://xp2.zedo.com/jsc/xp2/fo.js"></script><!-- end ZEDO for channel:  Quick Bytes LP , publisher: people , Ad Dimension: Medium Rectangle-300x250-QB-LP - 300 x 250 -->'

    #quickbytes_detail = QuickBytes.objects.raw("SELECT * FROM quick_bytes  WHERE quick_byte_id = "+quick_byte_id+" ")
    quickbytes_detail = QuickBytes.objects.filter(quick_byte_id = quick_byte_id).first()

    if quickbytes_detail:
        quick_byte_published_date = date(quickbytes_detail.quick_byte_published_date, 'd-m-Y')
        #date(self.birthdate, "n/j/Y")

        author_details = Author.objects.raw("SELECT AU.*, AUTYPE.* FROM author AU INNER JOIN quick_bytes QB ON QB.quick_byte_author_id = AU.author_id JOIN author_type AUTYPE ON AU.author_type = AUTYPE.author_type_id WHERE QB.quick_byte_id = "+quick_byte_id)
        if len(list(author_details)) > 0:
            author_label = author_details[0].label.replace(' ', '-')
        else:
            author_label = ''
        #author_label = author_details[0].label.replace(' ', '-')

        #quickbytes_tags = ChannelTags.objects.raw("SELECT t.* FROM channel_tags t INNER JOIN quick_bytes_tags qt ON t.tag_id = qt.tag_id WHERE qt.quick_byte_id = "+quick_byte_id)
        quickbytes_tags = ChannelTags.objects.raw("SELECT t.* FROM channel_tags t INNER JOIN quick_bytes_tags qt ON t.tag_id = qt.tag_id WHERE qt.quick_byte_id = "+quick_byte_id)
        tag_names = ''
        for tag in quickbytes_tags:
            tag_names = tag_names+', '+tag.tag_name

        '''quickbytes_topics = ChannelTopics.objects.raw("SELECT t.* FROM channel_topics t INNER JOIN quick_bytes_topic qt ON t.topic_id = qt.topic_id WHERE qt.quick_byte_id = "+quick_byte_id)
        topic_names = ''
        for topic in quickbytes_topics:
            topic_names = topic_names+', '+topic.topic_name'''

        #related_articles = QuickBytes.objects.raw("SELECT ar.*, ia.quick_byte_photo_url, ia.quick_byte_photo_name, COUNT(*) AS tagcount FROM (SELECT tag_id AS id FROM quick_bytes_tags WHERE quick_byte_id="+quick_byte_id+") AS t1 JOIN  quick_bytes_tags t2 ON t1.id=t2.tag_id JOIN quick_bytes_photos ia ON t2.quick_byte_id=ia.quick_byte_id JOIN quick_bytes ar ON t2.quick_byte_id=ar.quick_byte_id GROUP BY t2.quick_byte_id HAVING t2.quick_byte_id!="+quick_byte_id+" ORDER BY tagcount DESC")

        next_quick_byte = quickbytes_detail.get_next();
        prev_quick_byte = quickbytes_detail.get_prev();

        quick_bytes_image = QuickBytesPhotos.objects.filter(quick_byte_image_id = quick_byte_image_id).filter(quick_byte_id = quick_byte_id).first()
        all_image_sequence_count = QuickBytesPhotos.objects.filter(quick_byte_id = quick_byte_id).filter(Q(sequence=None) | Q(sequence=0)).count()
        if all_image_sequence_count > 1:
            next_quick_byte_pic = quick_bytes_image.get_next_pic_quick_byte()
            prev_quick_byte_pic = quick_bytes_image.get_prev_pic_quick_byte()
        else:
            next_quick_byte_pic = quick_bytes_image.get_next_pic_sequence()
            prev_quick_byte_pic = quick_bytes_image.get_prev_pic_sequence()
        #next_quick_byte_pic = quick_bytes_image.get_next_pic();
        #prev_quick_byte_pic = quick_bytes_image.get_prev_pic();

        if len(list(author_details)) > 0:
            if author_details[0].author_type != 1 and author_details[0].author_type != 2:
                meta_title = quickbytes_detail.quick_byte_title+'-'+author_details[0].author_name+' - BW people'
                meta_description = author_details[0].author_name+' - '+quickbytes_detail.quick_byte_description+', '+tag_names
            else:
                meta_title = quickbytes_detail.quick_byte_title+' - BW people'
                meta_description = quickbytes_detail.quick_byte_description+', '+tag_names
        else:
            meta_title = quickbytes_detail.quick_byte_title+' - BW people'
            meta_description = quickbytes_detail.quick_byte_description+', '+tag_names
        meta_keyword = tag_names

        og_title= quickbytes_detail.quick_byte_title
        og_url= '/quickbytes/'+quick_byte_title+'/'+quick_byte_published_date+'-'+quick_byte_id
        if not quick_bytes_image:
            og_image= settings.AWS_S3_BASE_URL + settings.BUCKET_PATH +'static_bwhr/images/BW-people-logo.jpg'
        else:
            og_image= quick_bytes_image.quick_byte_photo_url

        #sponsored_detail = Sponsoredposts.objects.raw("SELECT S.*, SI.image_url FROM sponsoredposts S LEFT JOIN sponsoredposts_images SI ON SI.sponsoredposts_id = S.sponsoredposts_id  ORDER BY S.sponsoredposts_published_date DESC LIMIT 2")
        #feeds_cric = feedparser.parse('http://bwcio.com/feed/')
        #feeds_bws = feedparser.parse('http://bwsmartcities.com/feed')
        #feeds_bwh = feedparser.parse('http://bwhotelier.com/feed/')

        closeDbConnection()

        return render(request, 'quickbytes/quickbytes_landing.html',{
            'quickbytes_detail': quickbytes_detail,
            #'quickbytes_related_articles': related_articles,
            'sidebar_recent_articles': sidebar_dta['sidebar_recent_articles'],
            'trending_now_topics': sidebar_dta['trending_now_topics'],
            'videomaster_listing': sidebar_dta['videomaster_listing'],
            'bwtv_cat_details': sidebar_dta['bwtv_cat_details'],
            'next_quick_byte': next_quick_byte,
            'prev_quick_byte': prev_quick_byte,
            'next_quick_byte_pic': next_quick_byte_pic,
            'prev_quick_byte_pic': prev_quick_byte_pic,
            'quick_bytes_image': quick_bytes_image,
            'author_details': author_details,
            'author_label': author_label,
            'quickbytes_tags': quickbytes_tags,
            'meta_title': meta_title,
            'meta_description': meta_description,
            'meta_keyword': meta_keyword,
            'og_title': og_title,
            'og_url': og_url,
            'og_image': og_image,
            #'sponsored_detail':sponsored_detail,
            #'feeds_cric':feeds_cric,
            #'feeds_bws':feeds_bws,
            #'feeds_bwh':feeds_bwh,
            'sidebar_zedo_ad': sidebar_zedo_ad,
        })
    else:
        meta_title = 'Quickbytes - BW people'
        meta_description = 'Quickbytes'
        meta_keyword = 'Quickbytes'

        og_title= 'Quickbytes - BW people'
        #og_url= article_detail[0].get_absolute_url
        og_image= settings.AWS_S3_BASE_URL + settings.BUCKET_PATH +'static_bwhr/images/BW-people-logo.jpg'

        return render(request, 'quickbytes/quickbytes_not_found.html',{
            'sidebar_recent_articles': sidebar_dta['sidebar_recent_articles'],
            'trending_now_topics': sidebar_dta['trending_now_topics'],
            'videomaster_listing': sidebar_dta['videomaster_listing'],
            'bwtv_cat_details': sidebar_dta['bwtv_cat_details'],
            #'category_jumlist': category_jumlist,
            'meta_title': meta_title,
            'meta_description': meta_description,
            'meta_keyword': meta_keyword,
            'og_title': og_title,
            #'og_url': og_url,
            'og_image': og_image,
            'sidebar_zedo_ad': sidebar_zedo_ad,
        })
    '''
    return render(request, 'quickbytes/quickbytes_images_loading.html',{
        'quickbytes_detail': quickbytes_detail,
        'next_quick_byte_pic': next_quick_byte_pic,
        'prev_quick_byte_pic': prev_quick_byte_pic,
        'quick_bytes_image': quick_bytes_image,
        'author_details': author_details,
        'author_label': author_label,
    })
    '''
def quickbyte_listing(request):
    sidebar_zedo_ad = '<!-- Javascript tag  --><!-- begin ZEDO for channel:  Category Pages , publisher: people , Ad Dimension: Medium Rectangle-300x250-CP - 300 x 250 --><script language="JavaScript">var zflag_nid="3336"; var zflag_cid="2"; var zflag_sid="1"; var zflag_width="300"; var zflag_height="250"; var zflag_sz="19"; </script><script language="JavaScript" src="http://xp2.zedo.com/jsc/xp2/fo.js"></script><!-- end ZEDO for channel:  Category Pages , publisher: Businessworld , Ad Dimension: Medium Rectangle-300x250-CP - 300 x 250 -->'
    sidebar_dta = sidebar_data()
    category_jumlist = category_jump_list()

    quick_bytes = QuickBytes.objects.raw("SELECT Q.*, QP.quick_byte_photo_url as image_url, QP.quick_byte_photo_name FROM quick_bytes Q LEFT JOIN quick_bytes_photos QP ON Q.quick_byte_id = QP.quick_byte_id GROUP BY Q.quick_byte_id ORDER BY Q.quick_byte_published_date DESC ")

    paginator = Paginator(list(quick_bytes), 10) # Show 6 articles per page

    page = request.GET.get('page')
    no_of_pages = range(1, paginator.num_pages+1)
    pg_url = page

    try:
        quick_bytes = paginator.page(page)
        page_no = int(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        quick_bytes = paginator.page(1)
        pg_url = 1
        page_no = 1

    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        page_no = 1
        quick_bytes = paginator.page(paginator.num_pages)


    adjacent_pages = 5

    #page_numbers = [n for n in \ range(paginator.num_pages - adjacent_pages, paginator.num_pages + adjacent_pages + 1) \ if n > 0 and n <= paginator.num_pages]
    page_numbers = [n for n in \
                    range(page_no - adjacent_pages, page_no + adjacent_pages + 1) \
                    if n > 0 and n <= page_no]

    meta_title = 'Trending Business Listicles - BW people - Page'+str(page_no)
    meta_description = 'Trending Business Stories and Listicles from India and across the world. Page '+str(page_no)+' BW people.'

    og_title = 'Trending Business Listicles - BW people - Page'+str(page_no)
    og_url = '/all-quickbytes'
    og_image = settings.AWS_S3_BASE_URL + settings.BUCKET_PATH +'static_bwhr/images/BW-people-logo.jpg'


    return render(request, 'quickbytes/listing_quick.html', {
        'quick_bytes': quick_bytes,
        'category_jumlist': category_jumlist,
        'sidebar_recent_articles': sidebar_dta['sidebar_recent_articles'],
        'trending_now_topics': sidebar_dta['trending_now_topics'],
        'videomaster_listing': sidebar_dta['videomaster_listing'],
        'bwtv_cat_details': sidebar_dta['bwtv_cat_details'],
        'sidebar_zedo_ad': sidebar_zedo_ad,
        'meta_title': meta_title,
        'meta_description': meta_description,

        'og_title': og_title,
        'og_url': og_url,
        'og_image':og_image,
        'page_numbers':page_numbers,
        'show_first': 1 not in page_numbers,
        'show_last': paginator.num_pages not in page_numbers,
        'last_page': paginator.num_pages
    })

def quickbytes_load(request, quick_byte_title, quick_byte_published_date, quick_byte_id):

    quickbytes_detail = QuickBytes.objects.raw("SELECT * FROM quick_bytes  WHERE quick_byte_id != "+quick_byte_id+" ")

    paginator = Paginator(list(quickbytes_detail), 1) # Show 6 articles per page

    page = request.GET.get('page')
    no_of_pages = range(1, paginator.num_pages+1)

    try:
        quickbytes = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        quickbytes = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        articles = paginator.page(paginator.num_pages)
    sidebar_dta = sidebar_data()

    closeDbConnection()

    return render(request, 'article/quickbytes_load.html', {
        "recent_articles": quickbytes,
        'no_of_pages': no_of_pages
    })
