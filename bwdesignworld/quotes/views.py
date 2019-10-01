# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.http import HttpResponse
import datetime
from django.http import Http404
from django.template import RequestContext, loader
import pprint
import re
import string
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger, InvalidPage
from django.conf import settings

from quotes.models import ChannelQuote, Quotesauthor, Quotetags
from bwdesignworld.utils import sidebar_data, category_jump_list, closeDbConnection

# Create your views here.

def quoteslanding(request, quote_author_name, quote_id):
    #quote_detail = ChannelQuote.objects.raw("SELECT * FROM channel_quote  WHERE quote_id = "+quote_id)
    #quote_detail = ChannelQuote.objects.filter(quote_id=quote_id).first()

    quote_detail = ChannelQuote.objects.raw("SELECT CQ.*, QA.*,Qt.* FROM channel_quote CQ LEFT JOIN quotesauthor QA ON CQ.q_author_id = QA.author_id  LEFT JOIN quotetags Qt ON Qt.tag_id = CQ.q_tags  WHERE CQ.quote_id = "+quote_id)
    #quote_author_name_for_url = quote_detail[0].author_name.strip().replace(' ', '-')

    '''quote_tags = []
    quote_tags_ids = quote_detail[0].q_tags.split(',')
    for tag in quote_tags_ids:
        tag_details = Quotetags.objects.filter(tag_id=tag).first()
        quote_tags.append(tag_details)'''

    next_quote = quote_detail[0].get_next()
    category_jumlist = category_jump_list()

    page_author_name = str(quote_detail[0].tag)
    meta_title = 'Latest Business and Financial Quotes, Inspirational Quotes - '+ str(quote_detail[0].tag)+' - BW Wellbeingworld'
    meta_description = str(quote_detail[0].quote_description)
    meta_keyword = 'Business Quotes, Financial Quotes, Inspirational Quotes, BW Wellbeingworld'

    og_title= 'Latest Business and Financial Quotes, Inspirational Quotes - '+ str(quote_detail[0].tag)+' - BW Wellbeingworld'
    og_url= '/quotes/'+quote_author_name+'-'+quote_id
    if (quote_detail[0].quotes_image ==''):
        og_image= settings.AWS_S3_BASE_URL + settings.BUCKET_PATH +'static/images/BW-wellness-logo.jpg'
       
    else:
        og_image= settings.AWS_S3_BASE_URL + settings.BUCKET_PATH + settings.QUOTES_IMAGE_PATH + quote_detail[0].quotes_image


    sidebar_zedo_ad = '<!-- Javascript tag  --><!-- begin ZEDO for channel:  Internal Pages , publisher: Businessworld , Ad Dimension: Medium Rectangle-300x250-IP - 300 x 250 --><script language="JavaScript">var zflag_nid="3336"; var zflag_cid="4"; var zflag_sid="1"; var zflag_width="300"; var zflag_height="250"; var zflag_sz="22"; </script><script language="JavaScript" src="http://xp2.zedo.com/jsc/xp2/fo.js"></script><!-- end ZEDO for channel:  Internal Pages , publisher: Businessworld , Ad Dimension: Medium Rectangle-300x250-IP - 300 x 250 -->'
    quote_listing = ChannelQuote.objects.raw("SELECT CQ.*, QA.*,Qt.* FROM channel_quote CQ LEFT JOIN quotesauthor QA ON CQ.q_author_id = QA.author_id LEFT JOIN quotetags Qt ON Qt.tag_id = CQ.q_tags  ORDER BY RAND() LIMIT 0,6")
    closeDbConnection()

    return render(request, 'quotes/quotes_landing.html',{
        'quote_detail': quote_detail[0],
        'quote_listing': quote_listing,
        'quote_author_name_for_url': quote_author_name,
        #'quote_tags': quote_tags,
        'next_quote': next_quote,
        'category_jumlist': category_jumlist,
        'meta_title': meta_title,
        'meta_description': meta_description,
        'meta_keyword': meta_keyword,
        'og_title': og_title,
        'og_url': og_url,
        'og_image': og_image,
        'sidebar_zedo_ad': sidebar_zedo_ad,
        'page_author_name': page_author_name,
    })


def quoteslisting(request):
    quote_listing = ChannelQuote.objects.raw("SELECT CQ.*, QA.*,Qt.* FROM channel_quote CQ LEFT JOIN quotesauthor QA ON CQ.q_author_id = QA.author_id LEFT JOIN quotetags Qt ON Qt.tag_id = CQ.q_tags  ORDER BY CQ.quote_update_at DESC")
    quote_author_name_for_url = quote_listing[0].quote_author_name_for_url

    category_jumlist = category_jump_list()

    meta_title = 'Inspirational Quotes, business quotes, wealth management quotes, finance quotes - BW Wellbeingworld'
    meta_description = 'Quotes from Warren Buffet, Jack Ma and many other business leaders about finance and wealth management'
    meta_keyword = 'Business Quotes, Financial Quotes, Inspirational Quotes, BW Wellbeingworld'

    og_title= 'Latest Business and Financial Quotes, Inspirational Quotes - '+ str(quote_listing[0].tag) +' - BW Wellbeingworld'
    og_url= '/all-quotes'
    if (quote_listing[0].quotes_image !=''):
        og_image= settings.AWS_S3_BASE_URL + settings.BUCKET_PATH +'static/images/BW-wellness-logo.jpg'
        
    else:
        og_image= quote_listing[0].quotes_image

    sidebar_zedo_ad = '<!-- Javascript tag  --><!-- begin ZEDO for channel:  Internal Pages , publisher: Wellbeingworld , Ad Dimension: Medium Rectangle-300x250-IP - 300 x 250 --><script language="JavaScript">var zflag_nid="3336"; var zflag_cid="4"; var zflag_sid="1"; var zflag_width="300"; var zflag_height="250"; var zflag_sz="22"; </script><script language="JavaScript" src="http://xp2.zedo.com/jsc/xp2/fo.js"></script><!-- end ZEDO for channel:  Internal Pages , publisher: Wellbeingworld , Ad Dimension: Medium Rectangle-300x250-IP - 300 x 250 -->'

    closeDbConnection()

    return render(request, 'quotes/quotes_listing.html',{
        'quote_listing': quote_listing,
        'quote_author_name_for_url': quote_author_name_for_url,
        #'quote_tags': quote_tags,
        
        'category_jumlist': category_jumlist,
        'meta_title': meta_title,
        'meta_description': meta_description,
        'meta_keyword': meta_keyword,
        'og_title': og_title,
        'og_url': og_url,
        'og_image': og_image,
        'sidebar_zedo_ad': sidebar_zedo_ad,
    })
